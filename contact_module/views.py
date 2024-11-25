from typing import Any
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView

import site_setting
import site_setting.models
from .forms import ContactFormsModel
from .models import ProfileModel


# Create your views here.


class ContactView(FormView):
    form_class = ContactFormsModel
    template_name = 'contact_module/contact.html'
    success_url = '/'
    
    def get_context_data(self,*args ,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        setting = site_setting.models.SiteSetting.objects.filter(is_main_setting = True).first()
        context['site_setting'] = setting
        return context
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfilePicView(CreateView):
    template_name = 'contact_module/profile-pic.html'
    model = ProfileModel
    fields = '__all__'
    success_url = '/'


class ProfileListView(ListView):
    template_name = 'contact_module/profile_list.html'
    model = ProfileModel
    context_object_name = 'profiles'
