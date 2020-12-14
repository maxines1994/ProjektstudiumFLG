from gtapp.utils import get_context
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

def home_view(request):
    c = get_context("Startseite","Startseite")
    return render(request, "home.html", c)

def tasks_view(request):
    c = get_context("Aufgaben","Aufgaben")
    return render(request, "tasks.html", c)

def tasks_list_assigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    return render(request, "tasks_list.html", c)

def tasks_list_notassigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    return render(request, "tasks_list.html", c)

class Tasks_list_assigned_view(TemplateView):
    pass

class Tasks_list_notassigned_view(TemplateView):
    pass