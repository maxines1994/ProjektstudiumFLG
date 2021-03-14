from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from gtapp.forms import *
from gtapp.models import LiveSettings
import barcode
from io import BytesIO
from barcode.writer import SVGWriter
import os


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

def barcodeView(request, *args, **kwargs):
    context = {}
    barcode_list_total = os.listdir("static/barcodes")

    barcode_list_L1 = []
    barcode_list_L2 = []
    barcode_list_L3 = []
    barcode_list_JOGA = []
    barcode_list_Kunden = []

    for item in barcode_list_total:
        item_path = ("barcodes/" + item)
        if item[0] == "1":
            barcode_list_L1.append(item_path)
        elif item[0] == "2":
            barcode_list_L2.append(item_path)
        elif item[0] == "3":
            barcode_list_L3.append(item_path)
        elif item[0] == "4":
            barcode_list_JOGA.append(item_path)
        else:
            barcode_list_Kunden.append(item_path)

    context["L1_Barcodes"] = barcode_list_L1
    context["L2_Barcodes"] = barcode_list_L2
    context["L3_Barcodes"] = barcode_list_L3
    context["JOGA_Barcodes"] = barcode_list_JOGA
    context["Kunden_Barcodes"] = barcode_list_Kunden

    return render(request, "BarcodeSheets.html", context)