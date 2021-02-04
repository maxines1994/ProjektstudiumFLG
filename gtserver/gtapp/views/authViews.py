from gtapp.utils import get_context
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.conf import settings
from django.contrib.auth.decorators import login_required

@login_required
def change_user_view(request):
    c = dict(users=get_user_model().objects.all())
    return render(request, "registration/change_user.html", c)

@login_required
def change_user_to_view(request, id):
    if request.user.is_authenticated and settings.DEBUG:
        login(request, get_user_model().objects.get(id=id))
        return redirect('/')
    else:
        return HttpResponse('Unauthorized', status=401)

