from django.db import models
from django.contrib.auth.models import User
from . import GtModelBasic

class Player(GtModelBasic):
    """
    Dieses Model erweitert die User-Tabelle um zusaetzliche Felder
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)