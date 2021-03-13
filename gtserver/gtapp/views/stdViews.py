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
    context = {
        "JOGA": ["",],
        "KUNDEN": ["",],
        "LIEFERANTEN": ["",],
        "SPIELLEITUNG": ["",],
    }
    return render(request, "workflows.html", context)

