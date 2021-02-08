from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='substract')
def substract(value, arg):
    result = int(value) - int(arg)
    return int(result)

@register.filter(name='divide')
def divide(value, arg):
    try:
        result = int(value) / int(arg)
        return int(result)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter(name='multiply')
def multiply(value, arg):
    result = int(value) * int(arg)
    return result

@register.filter(name='to_class_name')
def to_class_name(value):
    return value.__class__.__name__