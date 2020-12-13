from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.forms import Cust_order_form, Cust_order_det_form
from gtapp.models import CustOrder, CustOrderDet

class Cust_order_create_view(CreateView):
    form_class = Cust_order_form
    template_name = "CustOrderForm.html"

    def form_valid(self, form):
        new_cust_order = form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(new_cust_order.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Auftrag erstellen","Aufträge")
        return context


class Cust_order_alter_view(UpdateView):
    form_class = Cust_order_form
    template_name = "CustOrderForm.html"

    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = CustOrderDet.objects.filter(cust_order=self.get_object().pk)
        context["cust_order_no"] = self.get_object().pk
        context = get_context_back(context,"Auftrag ändern","Aufträge")
        return context

class Cust_order_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = CustOrder.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/cust_order/alter/" + str(self.object.cust_order.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Cust_order_det_create_view(CreateView):
    form_class = Cust_order_det_form
    template_name = "CustOrderForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position erstellen","Aufträge")
        return context

    def form_valid(self, form):
        form.instance.cust_order = CustOrder.objects.get(id=self.kwargs["cust_order"])
        form.save()
        return HttpResponseRedirect("/cust_order/alter/" + str(self.kwargs["cust_order"]) + "/")
    
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
    
class Cust_order_view(TemplateView):
    template_name = "CustOrder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = CustOrder.objects.all()
        context = get_context_back(context,"Auftragsliste","Aufträge")
        return context

