from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .models import UserProfile, Post


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label=_('Enter username'), max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text',
                                                             'name': 'username',
                                                             'placeholder': 'Username'}))

    password1 = forms.CharField(label=_('Set up a password'), max_length=50,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'type': 'password', 'name': 'pass',
                                           'placeholder': 'Password'}))

    password2 = forms.CharField(label=_('Confirm the password'), max_length=50,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'type': 'password', 'name': 'pass',
                                           'placeholder': '********'}))
    email = forms.EmailField(label='E-mail', max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'type': 'text', 'name': 'username',
                                        'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            message = _("The two password fields didn't match.")
            raise forms.ValidationError(message, code='invalid')
        return cd['password2']


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['avatar', 'first_name', 'last_name', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control form-control-lg',
                                             'id': 'formFileLg', 'type': 'file'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}
            ),
            'bio': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': _('Enter some info about you')}
            ),
        }


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Title',
        }))

    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'category', 'tags']
        widgets = {
            'author': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here',
                                             'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
