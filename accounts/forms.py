from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm, ChangePasswordForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users."""
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    """Form for updating users."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Email address'),
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Password'),
        })

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('First Name'),
            }
        )
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Last Name'),
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Email address'),
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Password'),
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Confirm Password'),
        })

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Email address'),
        })

class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('New Password'),
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Confirm New Password'),
        })

class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Current Password'),
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('New Password'),
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': _('Confirm New Password'),
        })

class Enable2FAForm(forms.Form):
    """Form for enabling 2FA."""
    
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': _('Enter verification code'),
                'autocomplete': 'off'
            }
        )
    )
