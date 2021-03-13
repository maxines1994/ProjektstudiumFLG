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
    context['barcodes'] = generateBarcodes()
    print(context['barcodes'])
    return render(request, "BarcodeSheets.html", context)

def generateBarcodes():
    binary = BytesIO()
    barcode_type = 'code128'
    root_barcode = 10420037
    barcode_increment = 592327
    max_barcode = 99900000

    next_barcode = root_barcode
    barcode_list = []

    while next_barcode <= max_barcode:
        new_barcode = barcode.get(barcode_type, str(next_barcode), writer=SVGWriter())
        barcode_filepath = 'static/barcodes/' + str(next_barcode)
        if not os.path.exists(barcode_filepath):
            new_file = new_barcode.save(barcode_filepath)
        barcode_list.append(barcode_filepath.replace('static/', '') + '.svg')
        next_barcode += barcode_increment

    return barcode_list