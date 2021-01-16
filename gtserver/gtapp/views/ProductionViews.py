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
