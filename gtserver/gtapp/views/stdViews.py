from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Task, TaskType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet, CustComplaint, CustComplaintDet, SuppComplaint, SuppComplaintDet
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
    ext_sys = request.user.groups.filter(name=JOGA).exists()
    if request.method == "POST":
        number = request.POST.get('boxnr')
        if CustOrder.objects.filter(box_no = str(number)).exists() and len(CustOrder.objects.filter(box_no = str(number))) < 2:
                #task setzen welches neu entsteht
                pass
        elif CustOrderDet.objects.filter(box_no = str(number)).exists() and len(CustOrderDet.objects.filter(box_no = str(number))) < 2:
            mylist = CustOrderDet.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == CustOrderDet.Status.AUFTRAG_FREIGEGEBEN:
                    #Task erscheint bei dem Boxscan in der Produktion, wo dann die Hebebühne gebaut werden soll & der Status wird auf 4 gesetzt
                    Task.set_task_cust_det(obj, 6, Timers.get_current_day())
                    set_status(obj.id, 2, 4)
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1
                elif obj.status == CustOrderDet.Status.LIEFERUNG_AN_KD_AUSSTEHEND:
                    #Task erscheint bei dem Boxscan beim Kundendienst, wo dann die Hebebühne an den Kunden übergeben werden soll und der Status wird auf 6 gesetzt
                    Task.set_task_cust_det(obj, 8, Timers.get_current_day())
                    set_status(obj.id, 2, 6)
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1   
                elif obj.status == CustOrderDet.Status.BESTELLT:
                    #Task beim Kunden für den Wareneingang
                    if request.user.groups.filter(name=C1).exists():
                        Task.set_task_cust_det(obj, 11, Timers.get_current_day())
                    elif request.user.groups.filter(name=K2).exists():
                        Task.set_task_cust_det(obj, 12, Timers.get_current_day())
                    elif request.user.groups.filter(name=C3).exists():
                        Task.set_task_cust_det(obj, 13, Timers.get_current_day())
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1
        elif SuppOrder.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(SuppOrder.objects.filter(box_no = str(number)).exclude(external_system = ext_sys)) < 2:
            #Status-Abfrage -> Joga Bestellung auf Bestellt um dann den Task "Wareneingang" auszulösen
            mylist = SuppOrder.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == SuppOrder.Status.BESTELLT:
                    Task.set_task_supp(obj, 4, Timers.get_current_day())
                    set_status(obj.id, 3, 4)
                    boxno_found = 1
                    SuppOrder.objects.filter(pk=obj.id).update(box_no='')
            
        elif SuppOrderDet.objects.filter(box_no = str(number)).exists() and len(SuppOrderDet.objects.filter(box_no = str(number))) < 2:
            pass

        elif CustComplaintDet.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(CustComplaintDet.objects.filter(box_no = str(number)).exclude(external_system = ext_sys)) < 2:
            mylist = CustComplaintDet.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN:
                    Task.set_task_custComplaintDet(obj, 28, Timers.get_current_day())
                    set_status(obj.id, 6, 4)
                    boxno_found = 1
                if obj.status == CustComplaintDet.Status.ANPASSUNG_ABGESCHLOSSEN:
                    Task.set_task_custComplaintDet(obj, 31, Timers.get_current_day())
                    set_status(obj.id, 6, 6)
                    boxno_found = 1
            CustComplaintDet.objects.filter(pk=obj.id).update(box_no='')

        elif SuppComplaint.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(SuppComplaint.objects.filter(box_no = str(number)).exclude(external_system = ext_sys)) < 2:
            mylist = SuppComplaint.objects.filter(box_no = str(number))
            print("Jo hier bin ich")
            for obj in mylist:
                if obj.status == SuppComplaint.Status.ERFASST:
                    set_status(obj.id, 7, 5)
                    Task.set_task_suppComplaint(obj, 36, Timers.get_current_day())
                    boxno_found = 1
                    SuppComplaint.objects.filter(pk=obj.id).update(box_no='')
                if obj.status == SuppComplaint.Status.WEITERLEITUNG_AN_PDL:
                    #set_status(obj.id, 7, 5)
                    Task.set_task_suppComplaint(obj, 34, Timers.get_current_day())
                    boxno_found = 1
                    SuppComplaint.objects.filter(pk=obj.id).update(box_no='')
    else:
        return render(request, "box.html")

    if boxno_found == 1: 
        return HttpResponseRedirect(reverse("tasks_notassigned"))
    else:
        c = {}
        c["FEHLER"] = 1
        return render(request, "box.html", c)

#Status und Task setzten
def set_status_task (request, **kwargs):
    
    set_status(kwargs["id"], kwargs["type"], kwargs["status"])
    #custorder
    if kwargs["type_for_task"] == 1:
        Task.set_task_cust(CustOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custorderdet
    elif kwargs["type_for_task"] == 2:
        Task.set_task_cust_det(CustOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #supporder
    elif kwargs["type_for_task"] == 3:
        Task.set_task_supp(SuppOrder.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #supporderdet
    elif kwargs["type_for_task"] == 4:
        Task.set_task_supp_det(SuppOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custcomplaint
    elif kwargs["type_for_task"] == 5:
        Task.set_task_custComplaint(CustComplaint.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custcomplaintdet
    elif kwargs["type_for_task"] == 6:
        Task.set_task_custComplaintDet(CustComplaintDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #suppcomplaint
    elif kwargs["type_for_task"] == 7:
        Task.set_task_suppComplaint(SuppComplaint.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    else:
        pass
    return HttpResponseRedirect(reverse("tasks_notassigned"))


#Status und Task setzten, Da für jede Position ein Task angelegt werden muss, gibt es hier eine spezielle Funktion dafür
# Durchläuft alle Positionen
def set_status_task_share (request, **kwargs):
    #custcomplaint freigegeben auf custcomplaintdet (Auftragsfreigabe Reklamationen)
    if kwargs["type_for_task"] == 6:
        mylist = list(CustComplaintDet.objects.filter(cust_complaint_id = kwargs["id"])) 
        for i in mylist:
            set_status(i.id, kwargs["type"], kwargs["status"])
            Task.set_task_custComplaintDet(i,kwargs["tasktype"],Timers.get_current_day())
    elif kwargs["type_for_task"] == 1: 
        mylist = list(CustOrderDet.objects.filter(cust_order_id = kwargs["id"]))  
        for i in mylist:
            set_status(i.id, kwargs["type"], kwargs["status"])
            Task.set_task_cust_det(i, kwargs["tasktype"], Timers.get_current_day())
    return HttpResponseRedirect(reverse("tasks_notassigned"))


# Status setzen bei Auftrag freigeben
def set_status_call(request, **kwargs):
    set_status(kwargs["id"], kwargs["type"], kwargs["status"])
    return HttpResponseRedirect(reverse("home"))


#Status setzen keine view
def set_status(id, type, status):
    #custorder achtung dieser wird für die Freigabe des Auftrags verwendet SONST wird nur mit CustOrderDet gearbeitet
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
    elif type == 5:
        CustComplaint.objects.filter(pk=id).update(status=status)
    elif type == 6:
        CustComplaintDet.objects.filter(pk=id).update(status=status)
    elif type == 7:
        SuppComplaint.objects.filter(pk=id).update(status=status)
    elif type == 8:
        SuppComplaintDet.objects.filter(pk=id).update(status=status)
    else:
        pass
    

# Startseite
def home_view(request):
    c = get_context("Startseite", "Startseite")
    return render(request, "home.html", c)

# Startseite Absprünge per Buttons zu Informationsseiten
class home_information_pages(TemplateView):
    template_name = "HomeInformationPages.html"

# FAQ
class faq_view(TemplateView):
    template_name = "FAQ.html"

# Task Schaltfläche
def tasks_view(request):
    c = get_context("Aufgaben", "Aufgaben")
    return render(request, "tasks.html", c)

# Zugewiesene Tasks View
def tasks_list_assigned_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    c['tasks'] = Task.objects.filter(user=request.user)
    c['Headline'] = "Mir zugewiesene Aufgaben"
    c['assigned'] = 1
    return render(request, "tasks_list.html", c)

# Nicht-zugewiesene Tasks View
def tasks_list_notassigned_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    myList = list()
    u = request.user.groups.all()
    for group in u:
        for i in Task.objects.filter(task_type__in=TaskType.objects.filter(group=group), user__isnull=True):
            myList.append(i)
    c["tasks"] = myList
    c['Headline'] = "Verfügbare Aufgaben"
    c['notassigned'] = 1
    return render(request, "tasks_list.html", c)

# Bearbeitete Tasks View
def tasks_list_finished_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    c['tasks'] = Task.objects.filter(user=request.user, active=0)
    c['Headline'] = "Abgeschlossene Aufgaben"
    c['finished'] = 1
    return render(request, "tasks_list.html", c)

# Weise Task User zu
def tasks_assign_to_me_view(request, **kwargs):
    Task.objects.filter(pk=kwargs["id"]).update(user=request.user)
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Weise Task Team zu
def tasks_share_to_team_view(request, **kwargs):
    Task.objects.filter(pk=kwargs["id"]).update(user_id = '')
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Beende Task
def tasks_finish(request, **kwargs):
    
    Task.objects.filter(pk=kwargs["id"]).update(active=0, finished_on=Timers.get_current_day())
    return HttpResponseRedirect(reverse("tasks_finished"))
    

# Bearbeite Task
def tasks_edit(request, **kwargs):
    mytask = Task.objects.filter(pk=kwargs["id"])[0]
    if mytask.task_type_id==1 or mytask.task_type_id == 16 or mytask.task_type_id == 17 or mytask.task_type_id == 18:
        return HttpResponseRedirect(reverse("cust_order_alter", kwargs={'id':mytask.cust_order.pk}))
    elif mytask.task_type_id == 2:
        #Bestandsprüfungsseite eintragen
        pass
    elif mytask.task_type_id == 19:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytask.supp_order.pk}))
    elif mytask.task_type_id == 20:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytask.supp_order.pk}))
    elif mytask.task_type_id == 21:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id == 22:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id == 23:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id == 27:
        return HttpResponseRedirect(reverse("cust_order_det_alter", kwargs={'id':mytask.cust_complaint_det.pk}))
    elif mytask.task_type_id == 28:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint_det.cust_complaint.pk}))
    elif mytask.task_type_id == 29:
         return HttpResponseRedirect(reverse("cust_order_det_alter", kwargs={'id':mytask.cust_complaint_det.pk}))
    elif mytask.task_type_id == 32:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 33:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 34:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 35:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 36:
        #Bestandsprüfung einbauen
        pass



# Task Detail View
class Tasks_detail_view(DetailView):
    template_name = "tasks_detail.html"
    model = Task

      # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = Task.objects.get(id=self.kwargs['id'])
        return obj


# Zentrale View für Async Javascript
def get_async_information(request, **kwargs):
    List = {}
    List["time"] = Timers.get_current_day()
    return HttpResponse(json.dumps(List))
