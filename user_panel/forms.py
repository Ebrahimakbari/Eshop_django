from django import forms
from account_module.models import User


class EditProfileFormsModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر',
            'address': 'ادرس',
            'about_user': 'درباره کاربر'
        }


class ChangePasswordForms(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'پسورد قبلی'
    }), label='پسورد قبلی')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'پسورد جدید'
    }), label='پسورد جدید')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'تکرار پسورد جدید'
    }), label='تکرار پسورد جدید')

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise forms.ValidationError('پسورد جدید با تکرار آن یکسان نیست')
        return confirm_new_password
