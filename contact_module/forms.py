from django import forms
from .models import ContactUs


class ContactForms(forms.Form):
    full_name = forms.CharField(
        label='نام',
        # error_messages={
        #     'required': 'this field should be filled'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام'
        })
    )
    email = forms.EmailField(label='ایمیل',
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'ایمیل'})
                             )
    title = forms.CharField(label='موضوع',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'موضوع'})
                              )
    message = forms.CharField(label='پیام',
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'پیام',
                                  'id': 'message'})
                              )

class ContactFormsModel(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'title', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'}),
            
            'email': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'ایمیل'
                }),
            'title': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'موضوع'
                }),
            'message': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'پیام',
                    'id': 'message'
                })
        }
        