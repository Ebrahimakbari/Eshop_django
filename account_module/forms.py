from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder':"ایمیل"}),
        validators=[validators.EmailValidator],
    )
    password = forms.CharField(
        label='پسورد',
        widget=forms.PasswordInput(attrs={'placeholder':"پسورد"}),
    )
    confirm_password = forms.CharField(
        label='تکرار پسورد',
        widget=forms.PasswordInput(attrs={'placeholder':"تکرار پسورد"}),
    )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('پسورد ها یکسان نیست')
        else:
            return password


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder':"ایمیل"}),
        validators=[validators.EmailValidator]
    )
    password = forms.CharField(
        label='پسورد',
        widget=forms.PasswordInput(attrs={'placeholder':"پسورد"})
    )

class ResetForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder':"ایمیل"}),
        validators=[validators.EmailValidator]
    )

class ResetPassForm(forms.Form):
    password = forms.CharField(
        label='پسورد',
        widget=forms.PasswordInput(attrs={'placeholder':"پسورد"}),
    )
    confirm_password = forms.CharField(
        label='تکرار پسورد',
        widget=forms.PasswordInput(attrs={'placeholder':"تکرار پسورد"}),
    )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('پسورد ها یکسان نیست')
        else:
            return password