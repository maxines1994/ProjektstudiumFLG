from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Todo, TodoType
from django.contrib.auth.models import Group, User
from gtapp.constants import *


# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

# Startseite
def home_view(request):
    c = get_context("Startseite","Startseite")
    return render(request, "home.html", c)

# Task Schaltfläche
def tasks_view(request):
    c = get_context("Aufgaben","Aufgaben")
    return render(request, "tasks.html", c)

# Zugewiesene Tasks View
def tasks_list_assigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    c['tasks'] = Todo.objects.filter(user=request.user)
    c['Headline'] = "Mir zugewiesene Aufgaben"
    return render(request, "tasks_list.html", c)

# Nicht-zugewiesene Tasks View
def tasks_list_notassigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    myList = list()
    u = request.user.groups.all()
    for group in u:
        for i in Todo.objects.filter(todo_type__in=TodoType.objects.filter(group=group),user_id=UNKNOWN):
            myList.append(i)
    c["tasks"] = myList
    c['Headline'] = "Verfügbare Aufgaben"
    return render(request, "tasks_list.html", c)

# Weise Task User zu
def tasks_assign_to_me_view(request, **kwargs):
    Todo.objects.filter(pk=kwargs["id"]).update(user=request.user)
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Weise Task Team zu
def tasks_share_to_team_view(request, **kwargs):
    Todo.objects.filter(pk=kwargs["id"]).update(user_id=UNKNOWN)
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Task Detail View
class Tasks_detail_view(DetailView):
    template_name = "tasks_detail.html"
    model = Todo

class Tasks_list_assigned_view(TemplateView):
    pass

class Tasks_list_notassigned_view(TemplateView):
    pass
