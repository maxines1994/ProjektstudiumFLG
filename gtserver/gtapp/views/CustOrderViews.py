from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.forms import Cust_order_form_jg, Cust_order_form_kd, Cust_order_det_form, Cust_order_det_form_create
from gtapp.models import CustOrder, CustOrderDet, Todo, Timers
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Max
from gtapp.constants.groups import *


# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_create_view(CreateView):
    template_name = "CustOrderForm.html"

    # Umleitung auf die Alter View
    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id
        if self.request.user.groups.filter(name='customer 1').exists():
            form.instance.customer_id = 1
        elif self.request.user.groups.filter(name='customer 2').exists():
            form.instance.customer_id = 2
        elif self.request.user.groups.filter(name='customer 3').exists():
            form.instance.customer_id = 3

        if self.request.user.groups.filter(name=CUSTOMERS).exists():
            form.instance.external_system = True

        new_cust_order = form.save()
        
        Todo.set_first_todo(new_cust_order, 1, Timers.get_current_day())
        
        return HttpResponseRedirect("/cust_order/alter/" + str(new_cust_order.pk) + "/")

    def get_initial(self):
        return {"issued_on":Timers.get_current_day()}

    # Navbar Context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name='customers').exists():
            form_class = Cust_order_form_kd
        else:
            form_class = Cust_order_form_jg
        return form_class(**self.get_form_kwargs()) 

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_alter_view(UpdateView):
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
        context["order_no"] = self.get_object().order_no
        context["action"] = "alter"
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name='customers').exists():
            form_class = Cust_order_form_kd
        else:
            form_class = Cust_order_form_jg
        return form_class(**self.get_form_kwargs()) 

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
    form_class = Cust_order_det_form_create
    template_name = "CustOrderDetForm.html"
    
#    def get(self, request, *args, **kwargs):
#        #Feld pos ausblenden
#        form = self.form_class(})
#        return render(request, self.template_name, {'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.cust_order = CustOrder.objects.get(id=self.kwargs["cust_order"])
        
        # Position vergeben
        try:
            form.instance.pos = CustOrderDet.objects.filter(cust_order=form.instance.cust_order).latest('_creation_date').pos + 1
        except CustOrderDet.DoesNotExist:
            form.instance.pos = 1
        
        newCustOrderDet=form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(self.kwargs["cust_order"]) + "/")

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_det_alter_view(UpdateView):
    form_class = Cust_order_det_form
    template_name = "CustOrderDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = CustOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance.pos = CustOrderDet.objects.get(id=form.instance.id).pos
        custOrderDet = form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(form.instance.cust_order.id) + "/")

#//self.kwargs["id"]

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

        if (False):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name=C1).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=1)
            elif self.request.user.groups.filter(name=C2).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=2)
            elif self.request.user.groups.filter(name=C3).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=3)
            else:
                context['orders'] = CustOrder.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name=C1).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=1, external_system=True)
            elif self.request.user.groups.filter(name=C2).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=2, external_system=True)
            elif self.request.user.groups.filter(name=C3).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=3, external_system=True)
            else:
                context['orders'] = CustOrder.objects.filter(external_system=False)

        return context
