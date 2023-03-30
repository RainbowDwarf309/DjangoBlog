from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm
# from .models import


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
