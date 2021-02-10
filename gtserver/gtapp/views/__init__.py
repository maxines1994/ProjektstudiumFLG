from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Task, TaskType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet, CustComplaint, CustComplaintDet, SuppComplaint, SuppComplaintDet
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
from gtapp.views import *
from django import forms
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json

# Reihenfolge alphabetisch / wie Dateibaum
from .ApiViews import *
from .AuthViews import *
from .BoxViews import *
from .cancelViews import *
from .CustComplaintViews import *
from .CustOrderViews import *
from .DeliveryViews import *
from .ManufacturingViews import *
from .messageViews import *
from .ProductionViews import *
from .StatusViews import *
from .stdViews import *
from .StockViews import *
from .SuppComplaintViews import *
from .SuppOrderViews import *
from .TaskViews import *
