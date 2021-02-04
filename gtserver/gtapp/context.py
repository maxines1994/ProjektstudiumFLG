from django.conf import settings
from gtapp.models import Timers, Task
from gtapp import constants
from gtapp.constants import *

#Global context

def gtcontext(request):
    if request.user.groups.filter(name=JOGA).exists():
        company = JOGA # light-blue
    elif request.user.groups.filter(name=LIEFERANTEN).exists():
        company = LIEFERANTEN # green
    elif request.user.groups.filter(name=KUNDEN).exists():
        company = KUNDEN # red
    else:
        company = 'none' # grey


    return {"debug_flag": settings.DEBUG, "company": company, "day": Timers.get_current_day(), "has_unassigned_tasks": Task.has_unassigned(request.user)}

def gtconstants(request):
    my_dict = {}

    #Durchlaufe alle Eintraege in den Konstanten, die Grossgeschrieben sind und nicht mit __ anfangen
    for item in dir(constants):
        if not item.startswith("__") and item.isupper():
            #Fuege den Eintrag dem Dictionary hinzu
            my_dict.update({item : str(getattr(constants, item))})
    
    #Liefere das gebildete Dictionary zurueck. Es enthaelt alle Konstanten aus dem constants-Ordner
    return my_dict   
    