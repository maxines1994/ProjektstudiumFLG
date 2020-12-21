from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
#from gtapp.forms import Cust_order_form, Cust_order_det_form
#from gtapp.models import CustOrder, CustOrderDet
from gtapp.models import SuppOrder, SuppOrderDet
from gtapp.forms import Supp_order_form, Supp_order_det_form

class Supp_order_create_view(CreateView):

    template_name = "SuppOrderForm.html"
    form_class = Supp_order_form

    #Gibt der Form mittels kwargs parameter des Users mit
    def get_form_kwargs(self):
        kwargs = super(Supp_order_create_view, self).get_form_kwargs()

        if self.request.method == 'GET':    
            groups = list(self.request.user.groups.values_list('name',flat = True))
            user_name = str(self.request.user)
            kwargs.update({
                'groups': str(groups[0]) ,
                'user_name': user_name,
            })

        return kwargs
    
    def form_valid(self, form):
        new_supp_order = form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(new_supp_order.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Auftrag erstellen","Aufträge")
        return context


class Supp_order_alter_view(UpdateView):
    form_class = Supp_order_form
    template_name = "SuppOrderForm.html"

    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = SuppOrderDet.objects.filter(supp_order=self.get_object().pk)
        context["supp_order_no"] = self.get_object().pk
        context = get_context_back(context,"Auftrag ändern","Aufträge")
        return context
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect("/supp_order/")

    #Gibt der Form mittels kwargs parameter des Users mit
    def get_form_kwargs(self):
        kwargs = super(Supp_order_alter_view, self).get_form_kwargs()

        if self.request.method == 'GET':    
            groups = list(self.request.user.groups.values_list('name',flat = True))
            user_name = str(self.request.user)
            kwargs.update({
                'groups': str(groups[0]) ,
                'user_name': user_name,
            })
        return kwargs
    
    

class Supp_order_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_order/"
        #success_url = "/supp_order/alter/" + str(self.object.supp_order.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Supp_order_det_create_view(CreateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position erstellen","Aufträge")
        return context

    def form_valid(self, form):
        form.instance.supp_order = SuppOrder.objects.get(id=self.kwargs["cust_order"])
        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.kwargs["cust_order"]) + "/")
    
class Supp_order_det_alter_view(UpdateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position ändern","Aufträge")
        return context

    def get_object(self, queryset=None):
        obj = SuppOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.object.supp_order.pk) + "/")

class Supp_order_det_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppOrderDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_order/alter/" + str(self.object.supp_order.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
class Supp_order_view(TemplateView):
    template_name = "SuppOrder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = SuppOrder.objects.all()
        context = get_context_back(context,"Auftragsliste","Aufträge")
        return context
