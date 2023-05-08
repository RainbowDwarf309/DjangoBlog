from django.conf import settings
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, View, ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token

from .forms import UserRegistrationForm, UserProfileUpdateForm, EmailChangeForm, NewsletterForm
from .models import UserProfile, Newsletter, ActionTrack, Post
from services.functions import track_action, get_summary_profile_data


class SignUpView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            new_email = user.email
            subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_letter.html', {
                'user': user,
                'domain': self.request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            messages.success(self.request, 'Please Confirm your email to complete registration.')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [new_email])
            return render(self.request, 'registration/registration_done.html', self.get_context_data())
        return render(self.request, 'registration/registration.html', self.get_context_data())


class UserLoginView(LoginView):
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if form.is_valid():
            return super(UserLoginView, self).form_valid(form)
        else:
            return render(self.request, self.template_name, self.get_context_data())


@method_decorator(login_required, name='dispatch')
class UserProfilePlatformView(UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    second_form_class = NewsletterForm
    template_name = 'news/user_profile_platform.html'

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfilePlatformView, self).get_context_data(**kwargs)
        user = self.request.user
        email = self.request.user.email
        subscriber, created = Newsletter.objects.get_or_create(user=user)
        choices = subscriber.choices.all()
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'sub_form' not in context:
            context['sub_form'] = self.second_form_class(initial={'user': user, 'email': email, 'choices': choices})
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_object(self, **kwargs):
        username = self.request.user.username
        if username is None:
            raise Http404
        return get_object_or_404(UserProfile, user__username__iexact=username)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.request.user
        email = self.request.user.email
        instance = Newsletter.objects.get(user=user)
        if 'profile-form' in request.POST:
            form_class = self.get_form_class()
            form_name = 'form'
        elif 'unsubscribe-sub-form' in request.POST:
            Newsletter.objects.filter(user=user, email=email).update(email=None, is_subscribed=False)
            instance.choices.clear()
            form_class = self.second_form_class
            form_name = 'sub_form'
        else:
            Newsletter.objects.filter(user=user).update(is_subscribed=True)
            subscriber, created = Newsletter.objects.get_or_create(user=user)
            self.object = subscriber
            form_class = self.second_form_class
            form_name = 'sub_form'
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})


@method_decorator(login_required, name='dispatch')
class UserProfilePublicationsView(ListView):
    template_name = 'news/user_profile_publications.html'
    model = Post
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        track_action(self.request, page=ActionTrack.AttrPage.USER_PROFILE_PUBLICATIONS,
                     action=ActionTrack.AttrAction.VIEW)
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class UserProfileSummaryView(TemplateView):
    template_name = 'news/user_profile_summary.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = get_summary_profile_data(self.request.user)
        track_action(self.request, page=ActionTrack.AttrPage.USER_PROFILE_SUMMARY, action=ActionTrack.AttrAction.VIEW)
        return context


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class ChangeEmailView(TemplateView):
    model = User
    template_name = 'registration/email_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        form = EmailChangeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EmailChangeForm(request.POST)
        if form.is_valid():
            user = self.request.user
            new_email = form.cleaned_data['email']
            User.objects.filter(username=user.username, email=user.email).update(email=new_email, is_active=False)
            subject = 'Activate Your Account'
            message = render_to_string('registration/account_activation_letter.html', {
                'user': user,
                'domain': request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            messages.success(request, 'Please Confirm your email to complete registration.')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [new_email], fail_silently=False)
            return HttpResponseRedirect(reverse("login"))
        else:
            return self.form_invalid(form)


class ActivateAccountView(View):

    @staticmethod
    def get(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account have been confirmed.')
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return HttpResponseRedirect(reverse("login"))
