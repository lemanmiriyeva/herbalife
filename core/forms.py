from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_('Confirm password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password'), 'class': 'form-control'}),
    )

    class Meta:
        model  = User
        fields = ['phone', 'first_name', 'last_name']
        widgets = {
            'phone':      forms.TextInput(attrs={'placeholder': '+994 50 000 00 00', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder': _('First name'), 'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'placeholder': _('Last name'), 'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        # Yalnız rəqəmlər və + saxla
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        if User.objects.filter(phone=cleaned).exists():
            raise forms.ValidationError(_('This phone number is already registered.'))
        return cleaned

    def clean(self):
        cd = super().clean()
        if cd.get('password1') != cd.get('password2'):
            raise forms.ValidationError(_('Passwords do not match.'))
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    phone    = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(attrs={'placeholder': '+994 50 000 00 00', 'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password'), 'class': 'form-control'}),
    )

    def clean(self):
        phone    = self.cleaned_data.get('phone', '').strip()
        password = self.cleaned_data.get('password', '')
        cleaned  = ''.join(c for c in phone if c.isdigit() or c == '+')
        user = authenticate(username=cleaned, password=password)
        if user is None:
            raise forms.ValidationError(_('Phone number or password is incorrect.'))
        if not user.is_active:
            raise forms.ValidationError(_('This account is inactive.'))
        self.cleaned_data['user'] = user
        return self.cleaned_data
