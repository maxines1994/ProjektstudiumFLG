from gtapp.utils import get_context
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from gtapp.constants import *
from qr_code.qrcode.utils import WifiConfig
import hashlib

@login_required
def change_user_view(request, view):
    if view=='debug':
        userqueryset = get_user_model().objects.all()
        
        users = []
        for user in userqueryset.exclude(groups__name=SPIELLEITUNG):
            users.append(user)
        for user in userqueryset.filter(groups__name=SPIELLEITUNG):
            users.append(user)

        c = dict(users=users)
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
        login(request, user)
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
        
        userqueryset = get_user_model().objects.exclude(groups__name=SPIELLEITUNG)

        users = []
        for user in userqueryset.filter(groups__name=KUNDEN):
            users.append(user)
        for user in userqueryset.filter(groups__name=JOGA):
            users.append(user)
        for user in userqueryset.filter(groups__name=LIEFERANTEN):
            users.append(user)

        userdict = []
        for user in users:
            password = str(int(hashlib.sha256(user.username.encode('utf-8')).hexdigest(), 16) % 10**4)
            credentials = {
                'user': user,
                'password': password,
                'company': user.groups.filter(name__in=[KUNDEN, JOGA, LIEFERANTEN]).first().name,
                'group': user.groups.exclude(name__in=[KUNDEN, JOGA, LIEFERANTEN]).first().name,
                'login_url': base_url + reverse('urllogin', kwargs={'username': user.username, 'password': password}),
            }
            userdict.append(credentials)
        
        wifi_config = WifiConfig(
            ssid='PLANSPIEL',
            authentication=WifiConfig.AUTHENTICATION.WPA,
            password='logisnet'
        )

        c = {'users': userdict, 'wifi_config': wifi_config}
        
        return render(request, "registration/credentials_sheet.html", c)
    else:
        return HttpResponse('Unauthorized', status=401)
