from gtapp.utils import get_context
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from gtapp.constants import *
import base64

@login_required
def change_user_view(request, view):
    if view=='debug':
        c = dict(users=get_user_model().objects.all())
    else:
        c = dict(users=get_user_model().objects.filter(groups__name=SPIELLEITUNG))
        
    return render(request, "registration/change_user.html", c)

@login_required
def change_user_to_view(request, id):
    if settings.DEBUG or request.user.groups.filter(name=SPIELLEITUNG).exists():
        login(request, get_user_model().objects.get(id=id))
        return redirect('/')
    else:
        return HttpResponse('Unauthorized', status=401)

# not at all safe, but convenient
def url_login_view(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return redirect('/')
    else:
        return HttpResponse('Unauthorized', status=401)

@login_required
def credentials_sheet_view(request):
    if settings.DEBUG or request.user.groups.filter(name=SPIELLEITUNG).exists():

        if request.is_secure():
            base_url = 'https://'
        else:
            base_url = 'http://'
        base_url += request.get_host()

        users = []
        for user in get_user_model().objects.exclude(groups__name=SPIELLEITUNG):
            password = base64.urlsafe_b64encode(user.username.encode("utf-8")).decode().replace("=", "")
            credentials = {
                'user': user,
                'password': password,
                'login_url': base_url + reverse('urllogin', kwargs={'username': user.username, 'password': password}),
            }
            users.append(credentials)
        
        c = {'users': users}
        
        return render(request, "registration/credentials_sheet.html", c)
    else:
        return HttpResponse('Unauthorized', status=401)
