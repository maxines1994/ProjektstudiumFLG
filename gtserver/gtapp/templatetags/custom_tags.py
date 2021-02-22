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

@register.filter(name='group_has_work')
def group_has_work(value, arg):
    try:
        return value.group_has_work(arg)
    except Exception as e:
        template = "[ERROR] Template-Tag 'group_has_work' in custom_tags.py: An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print (message)
        return False
