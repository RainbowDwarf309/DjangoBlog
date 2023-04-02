from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404

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
            form.save()
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

