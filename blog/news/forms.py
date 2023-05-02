import imghdr
from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from .models import Comment, UserProfile, Post, Newsletter
from mptt.forms import TreeNodeChoiceField


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
                                 attrs={'class': 'form-control', 'type': 'email', 'name': 'email',
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

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', None)
        if not avatar:
            raise ValidationError(_('Couldn\'t read image.'))
        try:
            if imghdr.what(avatar) != 'png':
                raise ValidationError(_('Image must be in .png format'))
            if avatar.size > settings.FORM_MAXIMUM_AVATAR_SIZE_BYTES:
                raise ValidationError(_('Image file too large ( > 0.5 mb )'))
            return avatar
        except ValidationError as e:
            raise e
        except FileNotFoundError:
            raise ValidationError(_('Couldn\'t read image. Please, update avatar.'))
        except Exception:
            raise ValidationError(_('Couldn\'t read image.'))

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
        fields = ['title', 'author', 'content', 'category', 'tags', 'link', 'photo']
        widgets = {
            'author': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here',
                                             'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'name': 'file'}),
            'link': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'Instagram link'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('The title must not begin with a number')
        return title


class CommentSubmitForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['post', 'parent', 'text']
        widgets = {
            'post': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '10',
                    'placeholder': _('Enter Your Comment Here'),
                }
            )
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(CommentSubmitForm, self).save(*args, **kwargs)


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control col-md-12', 'type': 'email',
                                        'placeholder': 'Enter your new email...'}))

    class Meta:
        model = User
        fields = ['email']


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['user', 'email', 'choices']
        widgets = {
            'user': forms.HiddenInput(),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'oninput': 'changeNewsletterForm("id_email");',
                    'placeholder': _('Enter your email...'),
                }),
            'choices': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'toggle-button',
                    'onchange': 'changeNewsletterForm(this.id);',
                }),
        }
        labels = {'choices': '', 'font-size': '13px',}

    def clean_email(self):
        cd = self.cleaned_data
        if Newsletter.objects.exclude(user=cd.get('user')).filter(email=cd.get('email')).exists():
            message = _('User with this email already exists')
            raise ValidationError(message)
        else:
            return cd['email']
