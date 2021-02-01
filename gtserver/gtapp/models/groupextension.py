from django.db import models
from django.contrib.auth.models import Group

"""
Hier wird die auth_group um neue Felder erweitert
"""
Group.add_to_class('code', models.CharField(max_length=3, null=True))
