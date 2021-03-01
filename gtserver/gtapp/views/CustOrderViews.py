from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.forms import Cust_order_form_jg, Cust_order_form_kd, Cust_order_det_form, Cust_order_det_fixed_form, Cust_order_det_form_create
from gtapp.models import CustOrder, CustOrderDet, Task, Timers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from gtapp.constants import *
from gtapp.models import LiveSettings



# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_create_view(LoginRequiredMixin, CreateView):
    template_name = "CustOrderForm.html"


    # Umleitung auf die Alter View
    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id
        
        if self.request.user.groups.filter(name=K1).exists():
            form.instance.customer_id = 1
        elif self.request.user.groups.filter(name=K2).exists():
            form.instance.customer_id = 2
        elif self.request.user.groups.filter(name=K3).exists():
            form.instance.customer_id = 3

        if self.request.user.groups.filter(name=KUNDEN).exists():
            form.instance.external_system = True

        new_cust_order = form.save()
        
        if form.instance.external_system == True:
            if self.request.user.groups.filter(name=K1).exists():
                Task.set_task(new_cust_order, 16)
            elif self.request.user.groups.filter(name=K2).exists():
                Task.set_task(new_cust_order, 17)
            elif self.request.user.groups.filter(name=K3).exists():
                Task.set_task(new_cust_order, 18)
        else:
            Task.set_task(new_cust_order, 1)
        
        return HttpResponseRedirect("/cust_order/alter/" + str(new_cust_order.pk) + "/")

    def get_initial(self):
        return {"issued_on":Timers.get_current_day()}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        context["status"] = None
        context["statuses"] = CustOrderDet.Status.__members__
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name=KUNDEN).exists():
            form_class = Cust_order_form_kd
        else:
            form_class = Cust_order_form_jg
        return form_class(**self.get_form_kwargs()) 

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_alter_view(LoginRequiredMixin, UpdateView):
    template_name = "CustOrderForm.html"
    success_url = "/cust_order/"


    # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj

    # Context zum Templating hinzufügen 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['items'] = CustOrderDet.objects.filter(cust_order=obj.pk)
        context["cust_order_no"] = obj.pk
        context["order_no"] = obj.order_no
        context["box_no"] = obj.box_no
        context["action"] = "alter"

        context["ORDER_STATUS"] = CustOrder.Status.__members__
        context["STATUS"] = CustOrderDet.Status.__members__
        #context["MIN_ITEM_STATUS"] = min(context['items'].values_list('status'))[0]
        context["MIN_ITEM_STATUS"] = 0
        context["can_cancel"] = CustOrderDet.objects.filter(cust_order=obj.id).count() > 0 and not CustOrderDet.objects.filter(cust_order=obj.id).exclude(status=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND).exclude(status=CustOrderDet.Status.STORNIERT).exists()
        context["can_delete"] = CustOrderDet.objects.filter(cust_order=obj.id).count() == 0 or not CustOrderDet.objects.filter(cust_order=obj.id).exclude(status=CustOrderDet.Status.ERFASST).exists()
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name=KUNDEN).exists():
            form_class = Cust_order_form_kd
        else:
            form_class = Cust_order_form_jg
        return form_class(**self.get_form_kwargs()) 

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_delete_view(LoginRequiredMixin, DeleteView):
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
class Cust_order_det_create_view(LoginRequiredMixin, CreateView):
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
class Cust_order_det_alter_view(LoginRequiredMixin, UpdateView):
    template_name = "CustOrderDetForm.html"

    def get_form_class(self):
        if self.get_object().status == CustOrderDet.Status.ERFASST:
            return Cust_order_det_form
        else:
            return Cust_order_det_fixed_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_no"] = self.get_object().box_no
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = CustOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance.pos = CustOrderDet.objects.get(id=form.instance.id).pos
        custOrderDet = form.save()
        if self.request.user.groups.filter(name=PRODUKTION).exists():
            return HttpResponseRedirect(reverse('manufacturing_list'))
        else:
            return HttpResponseRedirect("/cust_order/alter/" + str(form.instance.cust_order.id) + "/")

#//self.kwargs["id"]

# CustOrder von Joga und Bestellungen der Kunden
class Cust_order_det_delete_view(LoginRequiredMixin, DeleteView):
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
class Cust_order_view(LoginRequiredMixin, TemplateView):
    template_name = "CustOrder.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["STATUS"] = CustOrder.Status.__members__

        if (LiveSettings.objects.all().first().phase_3):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name=K1).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=1)
            elif self.request.user.groups.filter(name=K2).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=2)
            elif self.request.user.groups.filter(name=K3).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=3)
            else:
                context['orders'] = CustOrder.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name=K1).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=1, external_system=True)
            elif self.request.user.groups.filter(name=K2).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=2, external_system=True)
            elif self.request.user.groups.filter(name=K3).exists():
                context['orders'] = CustOrder.objects.filter(customer_id=3, external_system=True)
            else:
                context['orders'] = CustOrder.objects.filter(external_system=False)

        return context
