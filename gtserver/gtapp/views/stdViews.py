from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Todo, TodoType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
from django import forms
import json

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

#Boxnummer eintragen
class box_view(TemplateView):
    template_name = "box.html"

def box_search_view(request):
    boxno_found = 0
    if request.method == "POST":
        number = request.POST.get('boxnr')
        if CustOrder.objects.filter(box_no = str(number)).exists() and len(CustOrder.objects.filter(box_no = str(number))) < 2:
                #todo setzen welches neu entsteht
                pass
        elif CustOrderDet.objects.filter(box_no = str(number)).exists() and len(CustOrderDet.objects.filter(box_no = str(number))) < 2:
            mylist = CustOrderDet.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == str(3):
                    #Todo erscheint bei dem Boxscan in der Produktion, wo dann die Hebebühne gebaut werden soll & der Status wird auf 4 gesetzt
                    Todo.set_todo_cust_det(obj, 6, Timers.get_current_day())
                    set_status(obj.id,2,4)
                    boxno_found = 1
                elif obj.status == str(5):
                    #Todo erscheint bei dem Boxscan beim Kundendienst, wo dann die Hebebühne an den Kunden übergeben werden soll und der Status wird auf 6 gesetzt
                    Todo.set_todo_cust_det(obj, 8, Timers.get_current_day())
                    set_status(obj.id,2,6)
                    boxno_found = 1   
                elif obj.status == str(9):
                    #ToDo beim Kunden für den Wareneingang
                    if request.user.groups.filter(name=C1).exists():
                        Todo.set_todo_cust_det(obj, 11, Timers.get_current_day())
                    elif request.user.groups.filter(name=C2).exists():
                        Todo.set_todo_cust_det(obj, 12, Timers.get_current_day())
                    elif request.user.groups.filter(name=C3).exists():
                        Todo.set_todo_cust_det(obj, 13, Timers.get_current_day())
                    boxno_found = 1
        elif SuppOrder.objects.filter(box_no = str(number)).exists() and len(SuppOrder.objects.filter(box_no = str(number))) < 2:
            #Status-Abfrage -> Joga Bestellung auf Bestellt
            obj = SuppOrder.objects.get(box_no = str(number))
            for obj in mylist:
                if obj.status == 5:
                    Todo.set_todo_supp(obj, 4, Timers.get_current_day())
                    set_status(obj.id,3,4)
                    boxno_found = 1
            
        elif SuppOrderDet.objects.filter(box_no = str(number)).exists() and len(SuppOrderDet.objects.filter(box_no = str(number))) < 2:
            pass
            
    else:
        pass

    if boxno_found == 1: 
        return HttpResponseRedirect(reverse("tasks_notassigned"))
    else:
        return render(request, "box.html")

#Status und Todo setzten
def set_status_todo (request, **kwargs):
    set_status(kwargs["id"],kwargs["type"],kwargs["status"])
    #custorder
    if kwargs["type_for_todo"] == 1:
        Todo.set_todo_cust(kwargs["id"], kwargs["todotype"], Timers.get_current_day())
    #custorderdet
    elif kwargs["type_for_todo"] == 2:
        Todo.set_todo_cust_det(kwargs["id"], kwargs["todotype"], Timers.get_current_day())
    #supporder
    elif kwargs["type_for_todo"] == 3:
        print("HALLO " + str(kwargs["id"]))
        Todo.set_todo_supp(kwargs["id"], kwargs["todotype"], Timers.get_current_day())
    #supporderdet
    elif kwargs["type_for_todo"] == 4:
        Todo.set_todo_supp_det(kwargs["id"], kwargs["todotype"], Timers.get_current_day())
    else:
        pass
    return HttpResponseRedirect(reverse("tasks_notassigned"))


#Status und Todo setzten, Da für jede Position ein Todo angelegt werden muss, gibt es hier eine spezielle Funktion dafür
def set_status_todo_share (request, **kwargs):
    set_status(kwargs["id"],kwargs["type"],kwargs["status"])
    mylist = list(CustOrderDet.objects.filter(cust_order_id = kwargs["id"]))
    for i in mylist:
        Todo.set_todo_cust_det(i, kwargs["todotype"], Timers.get_current_day())
    return render(request, "home.html")


# Status setzen bei Auftrag freigeben
def set_status_call(request, **kwargs):
    set_status(kwargs["id"],kwargs["type"],kwargs["status"])
    return render(request, "home.html")

#Status setzen keine view
def set_status(id, type, status):
    #custorder
    if type == 1:
        mylist = list(CustOrderDet.objects.filter(cust_order_id = id))
        for i in mylist:
            CustOrderDet.objects.filter(pk=i.id).update(status=status)
    #custorderdet
    elif type == 2:
        CustOrderDet.objects.filter(pk=id).update(status=status)
    #supporder
    elif type == 3:
        SuppOrder.objects.filter(pk=id).update(status=status)
    #supporderdet
    elif type == 4:
        SuppOrderDet.objects.filter(pk=id).update(status=status)
    else:
        pass
    

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
    if mytodo.todo_type_id==1 or mytodo.todo_type_id == 16 or mytodo.todo_type_id == 17 or mytodo.todo_type_id == 18:
        return HttpResponseRedirect(reverse("cust_order_alter", kwargs={'id':mytodo.cust_order.pk}))
    elif mytodo.todo_type_id == 2:
        #Bestandsprüfungsseite eintragen
        pass
    elif mytodo.todo_type_id == 19:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytodo.supp_order.pk}))
    elif mytodo.todo_type_id == 20:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytodo.supp_order.pk}))

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
