from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Todo, TodoType, CustOrder
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
import json

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

# Startseite
def home_view(request):
    c = get_context("Startseite","Startseite")
    return render(request, "home.html", c)

# Startseite Absprünge per Buttons zu Informationsseiten
class Home_Information_Pages(TemplateView):
    template_name = "HomeInformationPages.html"

# Task Schaltfläche
def tasks_view(request):
    c = get_context("Aufgaben","Aufgaben")
    return render(request, "tasks.html", c)

# Zugewiesene Tasks View
def tasks_list_assigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    c['tasks'] = Todo.objects.filter(user=request.user)
    c['Headline'] = "Mir zugewiesene Aufgaben"
    c['assigned'] = 1
    return render(request, "tasks_list.html", c)

# Nicht-zugewiesene Tasks View
def tasks_list_notassigned_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    myList = list()
    u = request.user.groups.all()
    for group in u:
        for i in Todo.objects.filter(todo_type__in=TodoType.objects.filter(group=group),user__isnull=True):
            myList.append(i)
    c["tasks"] = myList
    c['Headline'] = "Verfügbare Aufgaben"
    c['notassigned'] = 1
    return render(request, "tasks_list.html", c)

# Bearbeitete Tasks View
def tasks_list_finished_view(request):
    c = get_context("Zugewiesene Aufgaben","Aufgaben")
    c['tasks'] = Todo.objects.filter(user=request.user, active=0)
    c['Headline'] = "Abgeschlossene Aufgaben"
    c['finished'] = 1
    return render(request, "tasks_list.html", c)

# Weise Task User zu
def tasks_assign_to_me_view(request, **kwargs):
    Todo.objects.filter(pk=kwargs["id"]).update(user=request.user)
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Weise Task Team zu
def tasks_share_to_team_view(request, **kwargs):
    Todo.objects.filter(pk=kwargs["id"]).update(user_id = '')
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Beende Task
def tasks_finish(request,**kwargs):
    
    Todo.objects.filter(pk=kwargs["id"]).update(active=0,finished_on=Timers.get_current_day())
    return HttpResponseRedirect(reverse("tasks_finished"))

# Bearbeite Task
def tasks_edit(request,**kwargs):
    mytodo = Todo.objects.filter(pk=kwargs["id"])[0]
    if mytodo.todo_type_id==1:
        return HttpResponseRedirect(reverse("cust_order_alter", kwargs={'id':mytodo.cust_order.pk}))


# Task Detail View
class Tasks_detail_view(DetailView):
    template_name = "tasks_detail.html"
    model = Todo

      # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = Todo.objects.get(id=self.kwargs['id'])
        return obj

# Zentrale View für Async Javascript
def get_async_information(request, **kwargs):
    List = {}
    List["time"] = Timers.get_current_day()
    return HttpResponse(json.dumps(List))
