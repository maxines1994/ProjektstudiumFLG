from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.forms import Cust_order_form, Cust_order_det_form
from gtapp.models import CustOrder, CustOrderDet
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max


# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_create_view(CreateView):
    form_class = Cust_order_form
    template_name = "CustOrderForm.html"

    # Umleitung auf die Alter View
    def form_valid(self, form):
        new_cust_order = form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(new_cust_order.pk) + "/")
    
    # Navbar Context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Auftrag erstellen","Aufträge")
        return context

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_alter_view(UpdateView):
    form_class = Cust_order_form
    template_name = "CustOrderForm.html"
    success_url = "/cust_order/"

    # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj

    # Context zum Templating hinzufügen 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = CustOrderDet.objects.filter(cust_order=self.get_object().pk)
        context["cust_order_no"] = self.get_object().pk
        context = get_context_back(context,"Auftrag ändern","Aufträge")
        return context

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_delete_view(DeleteView):
    template_name = "delete.html"
    success_url = "/cust_order/"

    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/cust_order/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_det_create_view(CreateView):
    form_class = Cust_order_det_form
    template_name = "CustOrderForm.html"
    
    #def get(self, request, *args, **kwargs):
    #    # Dynamisch Feld vorbelegen aus URLConf parameter pos # nun in form_valid gelöst
    #    form = self.form_class(initial={"pos": self.kwargs['pos']})
    #    return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position erstellen","Aufträge")
        return context

    def form_valid(self, form):
        form.instance.cust_order = CustOrder.objects.get(id=self.kwargs["cust_order"])

        # Position vergeben
        try:
            form.instance.pos = CustOrderDet.objects.filter(cust_order=form.instance.cust_order).latest('_creation_date').pos + 1
        except CustOrderDet.DoesNotExist:
            form.instance.pos = 1
        
        form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(self.kwargs["cust_order"]) + "/")

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_det_alter_view(UpdateView):
    form_class = Cust_order_det_form
    template_name = "CustOrderForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position ändern","Aufträge")
        return context

    def get_object(self, queryset=None):
        obj = CustOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(self.kwargs["id"]) + "/")

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_det_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = CustOrderDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/cust_order/alter/" + str(self.object.cust_order.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_view(TemplateView):
    template_name = "CustOrder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ToDo: Zusätzlichen Filter für Digitalisierungsstufe 1 einbauen, damit Kunden und JOGA nicht dieseleb Aufträge sehen können
        if self.request.user.groups.filter(name='customer 1').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=1)
        elif self.request.user.groups.filter(name='customer 2').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=2)
        elif self.request.user.groups.filter(name='customer 3').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=3)
        else:
            context['orders'] = CustOrder.objects.all()

        
        context = get_context_back(context,"Auftragsliste","Aufträge")
        return context
