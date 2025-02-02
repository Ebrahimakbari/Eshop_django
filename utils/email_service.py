from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages


def send_email(subject, context, to, template_name):
    try:
        html_message = render_to_string(template_name, context)
        text_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, text_message, from_email, [to], html_message=html_message)
        messages.success(context['request'],'email successfully sent')
    except:
        messages.error(context['request'],"email didn't sent")
