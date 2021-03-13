from . import *
from django.shortcuts import render
from django.template import RequestContext

# Anlegen von Views mit dictionary TITEL und Markierung für den User wo er sich gerade befindet.

# Startseite
@login_required
def home_view(request):
    c = get_context("Startseite", "Startseite")
    return render(request, "home.html", c)

# Startseite Absprünge per Buttons zu Informationsseiten
class home_information_pages(LoginRequiredMixin, TemplateView):
    template_name = "HomeInformationPages.html"

# FAQ
class faq_view(LoginRequiredMixin, TemplateView):
    template_name = "FAQ.html"

# HTTP Error 500
def handler500_view(request):
    return render(request, '500.html', status=500)

# HTTP Error 404
def handler404_view(request, exeption):
    return render(request, '404.html', status=404)

def workflows_view(request):
    img_path = "img/workflow/"
    context = {
        "JOGA": [   {"Title": "Hauptworkflow" , "Path":  img_path + "JOGA_Hauptworkflow.png"},
                    {"Title": "Bestellreklamation" , "Path": img_path + "JOGA_Bestellreklamation.png"}, 
                    {"Title": "Auftragsreklamationen" , "Path": img_path + "JOGA_Auftragsreklamation.png"},     
        ],

        "KUNDEN": [ {"Title": "Hauptworkflow" , "Path": img_path + "Kunden_Hauptworkflow.png"},
                    {"Title": "Bestellreklamation" , "Path": img_path + "Kunde_Bestellreklamation.png"},
        ],
        "LIEFERANTEN": [ {"Title": "Hauptworkflow" , "Path": img_path + "Lieferanten_Hauptworkflow.png"},
                         {"Title": "Auftragsreklamationen" , "Path": img_path + "Lieferanten_Auftragsreklamation.png"},
        ],
        "SPIELLEITUNG": [],
    }

    for item in context["JOGA"]:
        context["SPIELLEITUNG"].append({"Title": "JOGA - " + item["Title"], "Path": item["Path"]})
    for item in context["KUNDEN"]:
        context["SPIELLEITUNG"].append({"Title": "Kunden - " + item["Title"], "Path": item["Path"]})
    for item in context["LIEFERANTEN"]:   
        context["SPIELLEITUNG"].append({"Title": "Lieferanten - " + item["Title"], "Path": item["Path"]})

    workflows = []
    if request.user.groups.filter(name=JOGA).exists():
        workflows = context["JOGA"]
    elif request.user.groups.filter(name=KUNDEN).exists():
        workflows = context["KUNDEN"]
    elif request.user.groups.filter(name=LIEFERANTEN).exists():
        workflows = context["LIEFERANTEN"]
    elif request.user.groups.filter(name=SPIELLEITUNG).exists():
        workflows = context["SPIELLEITUNG"]
    return render(request, "workflows.html", {"workflows": workflows})

