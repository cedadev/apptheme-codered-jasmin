from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime

register = template.Library()

@register.filter
@stringfilter
def de_b(value):
    ''' If string value is prefixed as a bytecode (b'somestring', remove the wrapping b'')'''
    if value.startswith("b'"):
        return str(value.encode('utf-8'))[2:-1]
    else:
        return value

@register.filter(expects_localtime=True)
def datemod(value):
    '''manually truncate timezone (last 6 chars) off a string time value,
     then parse as datetime & return it'''
    datestr = value[:-6]
    newdate = datetime.strptime(datestr,'%a, %d %b %Y %H:%M:%S')
    return newdate

@register.filter(expects_localtime=True)
def dateage(value):
    '''return difference of a datetime versus now, in days'''
    deltadays = datetime.now() - value
    return deltadays.days

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)