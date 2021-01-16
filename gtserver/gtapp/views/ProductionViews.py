from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Todo, TodoType
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
import json

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

def Production_steps (request):
    c = get_context("Produktionsschritte","Produktionsschritte")
    return render(request, "ProductionSteps.html", c)

def M1_production_step_1(request):
    c = get_context("M1 Produktionsschritt 1","M1 Produktionsschritt 1")
    return render(request, "M1ProductionStep1.html", c)

def M1_production_step_2(request):
    c = get_context("M1 Produktionsschritt 2","M1 Produktionsschritt 2")
    return render(request, "M1ProductionStep2.html", c)

def M1_production_step_3(request):
    c = get_context("M1 Produktionsschritt 3","M1 Produktionsschritt 3")
    return render(request, "M1ProductionStep3.html", c)

def M1_production_step_4(request):
    c = get_context("M1 Produktionsschritt 4","M1 Produktionsschritt 4")
    return render(request, "M1ProductionStep4.html", c)

def M1_production_step_5(request):
    c = get_context("M1 Produktionsschritt 5","M1 Produktionsschritt 5")
    return render(request, "M1ProductionStep5.html", c)

def M1_production_step_6(request):
    c = get_context("M1 Produktionsschritt 6","M1 Produktionsschritt 6")
    return render(request, "M1ProductionStep6.html", c)

def M1_production_step_7(request):
    c = get_context("M1 Produktionsschritt 7","M1 Produktionsschritt 7")
    return render(request, "M1ProductionStep7.html", c)

def M1_production_step_8(request):
    c = get_context("M1 Produktionsschritt 8","M1 Produktionsschritt 8")
    return render(request, "M1ProductionStep8.html", c)

def M2_production_step_1(request):
    c = get_context("M2 Produktionsschritt 1","M2 Produktionsschritt 1")
    return render(request, "M2ProductionStep1.html", c)

def M2_production_step_2(request):
    c = get_context("M2 Produktionsschritt 2","M2 Produktionsschritt 2")
    return render(request, "M2ProductionStep2.html", c)

def M2_production_step_3(request):
    c = get_context("M2 Produktionsschritt 3","M2 Produktionsschritt 3")
    return render(request, "M2ProductionStep3.html", c)

def M2_production_step_4(request):
    c = get_context("M2 Produktionsschritt 4","M2 Produktionsschritt 4")
    return render(request, "M2ProductionStep4.html", c)

def M2_production_step_5(request):
    c = get_context("M2 Produktionsschritt 5","M2 Produktionsschritt 5")
    return render(request, "M2ProductionStep5.html", c)

def M2_production_step_6(request):
    c = get_context("M2 Produktionsschritt 6","M2 Produktionsschritt 6")
    return render(request, "M2ProductionStep6.html", c)

def M2_production_step_7(request):
    c = get_context("M2 Produktionsschritt 7","M2 Produktionsschritt 7")
    return render(request, "M2ProductionStep7.html", c)

def M2_production_step_8(request):
    c = get_context("M2 Produktionsschritt 8","M2 Produktionsschritt 8")
    return render(request, "M2ProductionStep8.html", c)

def M3_production_step_1(request):
    c = get_context("M3 Produktionsschritt 1","M3 Produktionsschritt 1")
    return render(request, "M3ProductionStep1.html", c)

def M3_production_step_2(request):
    c = get_context("M3 Produktionsschritt 2","M3 Produktionsschritt 2")
    return render(request, "M3ProductionStep2.html", c)

def M3_production_step_3(request):
    c = get_context("M3 Produktionsschritt 3","M3 Produktionsschritt 3")
    return render(request, "M3ProductionStep3.html", c)

def M3_production_step_4(request):
    c = get_context("M3 Produktionsschritt 4","M3 Produktionsschritt 4")
    return render(request, "M3ProductionStep4.html", c)

def M3_production_step_5(request):
    c = get_context("M3 Produktionsschritt 5","M3 Produktionsschritt 5")
    return render(request, "M3ProductionStep5.html", c)

def M3_production_step_6(request):
    c = get_context("M3 Produktionsschritt 6","M3 Produktionsschritt 6")
    return render(request, "M3ProductionStep6.html", c)

def M3_production_step_7(request):
    c = get_context("M3 Produktionsschritt 7","M3 Produktionsschritt 7")
    return render(request, "M3ProductionStep7.html", c)

def M3_production_step_8(request):
    c = get_context("M3 Produktionsschritt 8","M3 Produktionsschritt 8")
    return render(request, "M3ProductionStep8.html", c)

def M4_production_step_1(request):
    c = get_context("M4 Produktionsschritt 1","M4 Produktionsschritt 1")
    return render(request, "M4ProductionStep1.html", c)

def M4_production_step_2(request):
    c = get_context("M4 Produktionsschritt 2","M4 Produktionsschritt 2")
    return render(request, "M4ProductionStep2.html", c)

def M4_production_step_3(request):
    c = get_context("M4 Produktionsschritt 3","M4 Produktionsschritt 3")
    return render(request, "M4ProductionStep3.html", c)

def M4_production_step_4(request):
    c = get_context("M4 Produktionsschritt 4","M4 Produktionsschritt 4")
    return render(request, "M4ProductionStep4.html", c)

def M4_production_step_5(request):
    c = get_context("M4 Produktionsschritt 5","M4 Produktionsschritt 5")
    return render(request, "M4ProductionStep5.html", c)

def M4_production_step_6(request):
    c = get_context("M4 Produktionsschritt 6","M4 Produktionsschritt 6")
    return render(request, "M4ProductionStep6.html", c)

def M4_production_step_7(request):
    c = get_context("M4 Produktionsschritt 7","M4 Produktionsschritt 7")
    return render(request, "M4ProductionStep7.html", c)

def M4_production_step_8(request):
    c = get_context("M4 Produktionsschritt 8","M4 Produktionsschritt 8")
    return render(request, "M4ProductionStep8.html", c)