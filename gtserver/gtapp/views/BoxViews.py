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
                    Task.set_task(obj, 6)
                    set_status(obj.__class__, obj.id, CustOrderDet.Status.AUFTRAG_FREIGEGEBEN)
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1
                elif obj.status == CustOrderDet.Status.LIEFERUNG_AN_KD_AUSSTEHEND:
                    #Task erscheint bei dem Boxscan beim Kundendienst, wo dann die Hebebühne an den Kunden übergeben werden soll und der Status wird auf 6 gesetzt
                    Task.set_task(obj, 8)
                    set_status(obj.__class__, obj.id, CustOrderDet.Status.VERSANDT_AN_KD)
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1   
                elif obj.status == CustOrderDet.Status.BESTELLT:
                    #Task beim Kunden für den Wareneingang
                    if request.user.groups.filter(name=K1).exists():
                        Task.set_task(obj, 11)
                    elif request.user.groups.filter(name=K2).exists():
                        Task.set_task(obj, 12)
                    elif request.user.groups.filter(name=K3).exists():
                        Task.set_task(obj, 13)
                    CustOrderDet.objects.filter(pk=obj.id).update(box_no='')
                    boxno_found = 1
        elif SuppOrder.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(SuppOrder.objects.filter(box_no = str(number)).exclude(external_system = ext_sys)) < 2:
            #Status-Abfrage -> Joga Bestellung auf Bestellt um dann den Task "Wareneingang" auszulösen
            mylist = SuppOrder.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == SuppOrder.Status.BESTELLT:
                    Task.set_task(obj, 4)
                    set_status(obj.__class__ ,obj.id, SuppOrder.Status.BESTELLT)
                    boxno_found = 1
                    SuppOrder.objects.filter(pk=obj.id).update(box_no='')
            
        elif SuppOrderDet.objects.filter(box_no = str(number)).exclude(supp_order__external_system = ext_sys).exists() and len(SuppOrderDet.objects.filter(box_no = str(number)).exclude(supp_order__external_system = ext_sys)) < 2:
            pass

        elif CustComplaintDet.objects.filter(box_no = str(number)).exclude(cust_complaint__external_system = ext_sys).exists() and len(CustComplaintDet.objects.filter(box_no = str(number)).exclude(cust_complaint__external_system = ext_sys)) < 2:
            mylist = CustComplaintDet.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == CustComplaintDet.Status.VERSAND_AN_PRODUKTION:
                    Task.set_task(obj, 28)
                    set_status(obj.__class__, obj.id, CustComplaintDet.Status.IN_ANPASSUNG)
                    boxno_found = 1
                if obj.status == CustComplaintDet.Status.VERSAND_AN_KUNDENDIENST:
                    Task.set_task(obj, 31)
                    set_status(obj.__class__, obj.id, CustComplaintDet.Status.BEI_KUNDENDIENST)
                    boxno_found = 1
                if obj.status == CustComplaintDet.Status.VERSAND_AN_KUNDE:
                    set_status(obj.__class__, obj.id, CustComplaintDet.Status.GELIEFERT)
                    boxno_found = 1
            CustComplaintDet.objects.filter(pk=obj.id).update(box_no='')

        elif SuppComplaint.objects.filter(box_no = str(number)).exclude(external_system = ext_sys).exists() and len(SuppComplaint.objects.filter(box_no = str(number)).exclude(external_system = ext_sys)) < 2:
            mylist = SuppComplaint.objects.filter(box_no = str(number))
            for obj in mylist:
                if obj.status == SuppComplaint.Status.ERFASST:
                    set_status(obj.__class__, obj.id,SuppComplaint.Status.BESTANDSPRUEFUNG_AUSSTEHEND)
                    Task.set_task(obj, 36)
                    boxno_found = 1
                    SuppComplaint.objects.filter(pk=obj.id).update(box_no='')
                if obj.status == SuppComplaint.Status.WEITERLEITUNG_AN_PDL:
                    #set_status(obj.id, 7, 5)
                    Task.set_task(obj, 34)
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
            ## KUNDE
            if obj.cust_complaint.external_system:
                if obj.status == CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN:
                    return CustComplaintDet.Status.IN_REKLAMATION
            ## JOGA
            else:
                if obj.status == CustComplaintDet.Status.REKLAMATION_FREIGEGEBEN:
                    return CustComplaintDet.Status.VERSAND_AN_PRODUKTION
                elif obj.status == CustComplaintDet.Status.ANPASSUNG_ABGESCHLOSSEN:
                    return CustComplaintDet.Status.VERSAND_AN_KUNDENDIENST
                elif obj.status == CustComplaintDet.Status.BEI_KUNDENDIENST:
                    return CustComplaintDet.Status.VERSAND_AN_KUNDE



        else:
            return obj.status

    def form_valid(self, form):
        my_obj = self.get_object()
        form.instance.status = self.get_new_status(my_obj)
        my_obj = form.save()
        previous = self.request.POST.get('previous', '/')
        # Lieferanten werden weiter geleitet  auf die SuppOrder geleitet
        if self.request.user.groups.filter(name=LIEFERANTEN).exists():
            my_redirect = reverse("goods_shipping", args=('SuppOrder',self.kwargs['id']))
        else:
            # redirect zur Seite von der man urspruenglich kam
            my_redirect = previous
        return HttpResponseRedirect(my_redirect)
