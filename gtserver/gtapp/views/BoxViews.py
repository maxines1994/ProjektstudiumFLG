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
from gtapp.forms import *
import json



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
