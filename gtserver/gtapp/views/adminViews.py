from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from gtapp.forms import *
from gtapp.models import LiveSettings


class LiveSettingsForm(ModelForm):
    
    class Meta:
        model = LiveSettings
        fields = ["timelength"]
        labels = {
            "timelength": "Sekunden pro Zeiteinheit"
        }

class LiveSettingsUpdate(UpdateView):
    form_class = LiveSettingsForm
    model = LiveSettings
    template_name = "settings.html"
    success_url ="/options/"

    def get_object(self, *args, **kwargs):
        return LiveSettings.load()

def controlPanel(request):
    context = {"timeactive": LiveSettings.load().timeactive}
    return render(request,"controlpanel.html",context)

def timeToggleView(request, *args, **kwargs):
    dataset = LiveSettings.load()
    if dataset.timeactive:
        dataset.timeactive = False
    else:
        dataset.timeactive = True
    dataset.save()
    return HttpResponseRedirect(reverse("controlpanel"))
