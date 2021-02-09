from . import *

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