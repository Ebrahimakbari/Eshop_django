from django.shortcuts import redirect
from django.urls import reverse


def user_level_decorator_factory(data=None):
    def user_level_decorator(func):
        def wrapper(request,*args, **kwargs):
            if request.user.is_authenticated and request.user.is_superuser:
                return func(request,*args, **kwargs)
            else:
                return redirect(reverse('login_page'))
        return wrapper
    return user_level_decorator