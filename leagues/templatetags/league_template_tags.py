from django.template.defaulttags import register

import math

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_speed(speed, type):
    if type == '0':
        return (speed * 2) + 36
    elif type == '252':
        return math.floor((speed * 2) + 36 + (252/4))
    elif type == '252+':
        return math.floor(((speed * 2) + 36 + (252/4)) * 1.1)
    elif type == '+1':
        return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 1.5)
    elif type == '+2':
        return math.floor(math.floor((((speed * 2) + 36 + (252/4)) * 1.1)) * 2)