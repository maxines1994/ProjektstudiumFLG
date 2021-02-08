from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView, View
from gtapp.models import Task, TaskType
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
from gtapp.models.productionsteps import ProductionSteps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

@login_required
def production_steps(request):
    c = get_context("Produktionsschritte", "Produktionsschritte")
    return render(request, "ProductionSteps.html", c)

class production_steps_single(LoginRequiredMixin, TemplateView):
    template_name = "ProductionStepsSingle.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productionsteps_list'] = ProductionSteps.objects.all()
        return context

class production_steps_3D_models(LoginRequiredMixin, TemplateView):
    template_name = "ProductionSteps3DModels.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context