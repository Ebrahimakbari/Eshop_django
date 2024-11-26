from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from utils.email_service import send_email
from .forms import RegisterForm,LoginForm,ResetForm,ResetPassForm
from .models import User
from django.utils.crypto import get_random_string
from django.http import Http404, HttpRequest
from django.contrib.auth import login,logout



class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request,'account_module/register_page.html',context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data['email']
            user_password = register_form.cleaned_data['password']
            user:bool = User.objects.filter(email__exact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل از قبل موجود است')
            else:
                new_user = User(email=user_email,
                                username=user_email,
                                is_active=False,
                                email_verification=get_random_string(72)
                                )
                new_user.set_password(user_password)
                new_user.save()
                host =request.META['HTTP_HOST']
                send_email('فعال سازی اکانت',{'user':new_user,'host':host,'request':request},new_user.email,'emails/active_account.html')
                return redirect(reverse('login_page'))
        context = {'register_form': register_form}
        return render(request,'account_module/register_page.html',context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request,'account_module/login_page.html',context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact = email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email','حساب کاربری فعال نشده است')
                else:
                    is_pass_correct = user.check_password(password)
                    if is_pass_correct:
                        login(request,user)
                        return redirect(reverse('user_panel'))
                    else:
                        login_form.add_error(field='password',error='پسورد اشتباه است')
            else:
                login_form.add_error(field='email',error='ثبت نام نشده است')
        else:
            pass
        context = {'login_form': login_form}
        return render(request,'account_module/login_page.html',context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))

class ActivateAccount(View):
    def get(self,request,activate_code):
        user: User = User.objects.filter(email_verification__iexact = activate_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_verification = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                # todo: show message already activated
                pass
        raise Http404


class ResetView(View):
    def get(self, request):
        reset_form = ResetForm()
        context = {'reset_form': reset_form}
        return render(request,'account_module/reset_pass_page.html',context)
    
    def post(self,request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            email = reset_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact = email)
            if user is not None:
                host = request.META['HTTP_HOST']
                send_email('بازیابی کلمه عبور',{'user':user,'host':host,'request':request},user.email,'emails/reset_password.html')
                return redirect(reverse('login_page'))
        context = {'reset_form': reset_form}
        return render(request,'account_module/reset_pass_page.html',context)
        
        
class ResetPassView(View):
    def get(self,request,email_activate_code):
        reset_pass_form = ResetPassForm()
        user = User.objects.filter(email_verification__iexact = email_activate_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        
        context = {'reset_pass_form': reset_pass_form,
                    'user': user}
        return render(request,'account_module/reset_password.html',context)
    
    def post(self,request,email_activate_code):
        reset_pass_form = ResetPassForm(request.POST)
        if reset_pass_form.is_valid():
            user = User.objects.filter(email_verification__iexact = email_activate_code).first()
            if user is None:
                return redirect(reverse('login_page'))
            
            new_pass = reset_pass_form.cleaned_data.get('password')
            user.set_password(new_pass)
            user.email_verification = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {'reset_pass_form': reset_pass_form,
                    'user': user}
        return render(request,'account_module/reset_password.html',context)