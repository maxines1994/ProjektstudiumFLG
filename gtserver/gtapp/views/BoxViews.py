from gtapp.views.StatusViews import *
from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Task, TaskType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet, GtModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
from django import forms
from django.contrib.auth.decorators import login_required
from gtapp.forms import *
import json

#Boxnummer eintragen
class box_view(LoginRequiredMixin, TemplateView):
    template_name = "box.html"


@login_required
def box_search_view(request):
    boxno_found = 0
    ext_sys = request.user.groups.filter(name=JOGA).exists()
    if request.method == "POST":
        number = request.POST.get('boxnr')
        if CustOrder.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(CustOrder.objects.filter(box_no = str(number).exclude(external_system = ext_sys))) < 2:
                #task setzen welches neu entsteht
                pass
        elif CustOrderDet.objects.filter(box_no = str(number)).exclude(cust_order__external_system = ext_sys).exists() and len(CustOrderDet.objects.filter(box_no = str(number)).exclude(cust_order__external_system = ext_sys)) < 2:
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
                    if request.user.groups.filter(name=K1).exists():
                        Task.set_task_cust_det(obj, 11, Timers.get_current_day())
                    elif request.user.groups.filter(name=K2).exists():
                        Task.set_task_cust_det(obj, 12, Timers.get_current_day())
                    elif request.user.groups.filter(name=K3).exists():
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
            
        elif SuppOrderDet.objects.filter(box_no = str(number)).exclude(supp_order__external_system = ext_sys).exists() and len(SuppOrderDet.objects.filter(box_no = str(number)).exclude(supp_order__external_system = ext_sys)) < 2:
            pass

        elif CustComplaintDet.objects.filter(box_no = str(number)).exclude(cust_complaint__external_system = ext_sys).exists() and len(CustComplaintDet.objects.filter(box_no = str(number)).exclude(cust_complaint__external_system = ext_sys)) < 2:
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


class Box_assign_view(LoginRequiredMixin, UpdateView):
    template_name = "BoxAssign.html"
    form_class = Box_form

    # Model getten fuer das die Boxnummer eingetragen werden soll
    def get_model(self, **kwargs):
        return GtModel.str_to_gtmodel(self.kwargs['model'])

    # Objekt getten
    def get_object(self, queryset=None):
        model = self.get_model()
        obj = model.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_new_status(self, obj, **kwargs):
        """
        Bei jedem Model werden nur an einer Stelle im Workflow Boxnummern offiziell zugewiesen.
        Diese Funktion gibt anhand des Models den Status zurueck, den das Objekt bekommen soll
        nachdem eine Boxnummer zugewiesen wurde.
        """
        model = self.get_model()
        if model == CustOrderDet:
            return CustOrderDet.Status.VERSANDT_AN_KD
        elif model == SuppComplaint:
            return SuppComplaint.Status.ERLEDIGT
        elif model == CustComplaintDet:
            return CustComplaintDet.Status.ERLEDIGT
        else:
            return obj.Status

    def form_valid(self, form):
        my_obj = self.get_object()
        form.instance.status = self.get_new_status(my_obj)
        my_obj = form.save()
        # redirect zur Seite von der man urspruenglich kam
        previous = self.request.POST.get('previous', '/')
        return HttpResponseRedirect(previous)
