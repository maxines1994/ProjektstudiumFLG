from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import SuppOrder, SuppOrderDet, CustOrderDet, ArtiPart, Stock, Task, Part, Supplier
from gtapp.forms import Supp_order_form_jg, Supp_order_form_lf, Supp_order_det_form
from gtapp.models import LiveSettings
from gtapp.constants import *
from gtapp.models import Timers
from django.contrib.auth.mixins import LoginRequiredMixin


class Supp_order_create_view(LoginRequiredMixin, CreateView):
    template_name = "SuppOrderForm.html"

    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id
        
        if self.request.user.groups.filter(name=L100).exists():
            form.instance.supplier_id = 1
        elif self.request.user.groups.filter(name=L200).exists():
            form.instance.supplier_id = 2
        elif self.request.user.groups.filter(name=L300).exists():
            form.instance.supplier_id = 3
        
        if self.request.user.groups.filter(name=LIEFERANTEN).exists():
            form.instance.external_system = True
            
        new_supp_order = form.save()
        
        if self.request.user.groups.filter(name=L300).exists():
            Task.set_task(new_supp_order, 20)
        elif self.request.user.groups.filter(name=JOGA).exists():
            Task.set_task(new_supp_order, 19)
        

        return HttpResponseRedirect("/supp_order/alter/" + str(new_supp_order.pk) + "/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name=LIEFERANTEN).exists():
            form_class = Supp_order_form_lf
        else:
            form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs())
    
    def get_initial(self):
        return {
            "issued_on":Timers.get_current_day(),
            "supplier": 3
        }



class Supp_order_alter_view(LoginRequiredMixin, UpdateView):
    template_name = "SuppOrderForm.html"

    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = SuppOrderDet.objects.filter(
            supp_order=self.get_object().pk)
        context['supp_order_no'] = self.get_object().pk
        context["order_no"] = self.get_object().order_no
        context["box_no"] = self.get_object().box_no
        context["action"] = "alter"
        context["STATUS"] = SuppOrder.Status.__members__
        return context

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_order/")

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name=LIEFERANTEN).exists():
            form_class = Supp_order_form_lf
        else:
            form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs())


class Supp_order_delete_view(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"


    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_order/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Supp_order_det_create_view(LoginRequiredMixin, CreateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_order_det_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        if self.request.user.groups == LIEFERANTEN:
            parts = Part.objects.filter(supplier__name=self.request.user.groups.first())
        else:
            parts = Part.objects.all()
        kwargs.update({'parts': parts})
        return kwargs

    def form_valid(self, form):
        form.instance.supp_order = SuppOrder.objects.get(
            id=self.kwargs["supp_order"])
        form.instance._creation_user_id = self.request.user.id

        # Position vergeben
        try:
            form.instance.pos = SuppOrderDet.objects.filter(supp_order=form.instance.supp_order).latest('_creation_date').pos + 1
        except SuppOrderDet.DoesNotExist:
            form.instance.pos = 1


        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.kwargs["supp_order"]) + "/")
        


class Supp_order_det_alter_view(LoginRequiredMixin, UpdateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = SuppOrderDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_order_det_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        parts = Part.objects.filter(supplier__name=self.request.user.groups.first())
        kwargs.update({'parts': parts})
        return kwargs


    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.object.supp_order.pk) + "/")


class Supp_order_det_delete_view(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_order/alter/" + \
            str(self.object.supp_order.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)


class Supp_order_view(LoginRequiredMixin, TemplateView):
    template_name = "SuppOrder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["STATUS"] = SuppOrder.Status.__members__

        if (LiveSettings.objects.all().first().phase_3):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name=L100).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 1)
            elif self.request.user.groups.filter(name=L200).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 2)
            elif self.request.user.groups.filter(name=L300).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 3)
            else:
                context['orders'] = SuppOrder.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name=L100).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 1, external_system=True).exclude(pk__in=[1,2,3,4,5,6])
            elif self.request.user.groups.filter(name=L200).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 2, external_system=True).exclude(pk__in=[1,2,3,4,5,6])
            elif self.request.user.groups.filter(name=L300).exists():
                context['orders'] = SuppOrder.objects.filter(supplier_id = 3, external_system=True).exclude(pk__in=[1,2,3,4,5,6])
            else:
                context['orders'] = SuppOrder.objects.filter(external_system=False).exclude(pk__in=[1,2,3,4,5,6])
       
        return context
