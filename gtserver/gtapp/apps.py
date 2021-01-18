from django.apps import AppConfig

from django import template
register = template.Library()

class GtappConfig(AppConfig):
    name = 'gtapp'
