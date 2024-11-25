from django import template
from jalali_date import date2jalali


register = template.Library()

@register.filter('show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)

@register.filter('show_jalali_time')
def show_jalali_time(value):
    return value.strftime('%H:%M')

@register.filter('three_digits')
def three_digits(value):
    return '{:,}'.format(value) + 'تومان'

@register.filter('to_str')
def to_str(value):
    """converts int to string"""
    return str(value)