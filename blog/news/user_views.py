from django.conf import settings
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from .token import account_activation_token

from .forms import UserRegistrationForm, UserProfileUpdateForm
from .models import UserProfile


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
    template_name = 'news/user_profile_platform.html'

    def get_success_url(self):
        return self.request.path

    def get_object(self, **kwargs):
        username = self.request.user.username
        if username is None:
            raise Http404
        return get_object_or_404(UserProfile, user__username__iexact=username)


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
