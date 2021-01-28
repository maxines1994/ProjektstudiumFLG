from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import SuppOrder, SuppOrderDet, CustOrderDet, ArtiPart, Stock, Todo
from gtapp.forms import Supp_order_form_jg, Supp_order_form_lf,Supp_order_det_form
from django.db.models import Q
from gtapp.constants.groups import *
from gtapp.models import Timers


class Supp_order_create_view(CreateView):
    template_name = "SuppOrderForm.html"

    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id
        if self.request.user.groups.filter(name='supplier 100').exists():
            form.instance.supplier_id = 1
        elif self.request.user.groups.filter(name='supplier 200').exists():
            form.instance.supplier_id = 2
        elif self.request.user.groups.filter(name='supplier 300').exists():
            form.instance.supplier_id = 3
        
        if self.request.user.groups.filter(name=SUPPLIERS).exists():
            form.instance.external_system = True
            
        new_supp_order = form.save()
        
        if self.request.user.groups.filter(name='supplier 300').exists():
            Todo.set_todo_supp(new_supp_order, 20, Timers.get_current_day())
        elif self.request.user.groups.filter(name='JOGA').exists():
            Todo.set_todo_supp(new_supp_order, 19, Timers.get_current_day())
        

        return HttpResponseRedirect("/supp_order/alter/" + str(new_supp_order.pk) + "/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name='suppliers').exists():
            form_class = Supp_order_form_lf
        else:
            form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs())
    
    def get_initial(self):
        return {"issued_on":Timers.get_current_day()}

class Supp_order_alter_view(UpdateView):
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
        return context

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_order/")

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name='suppliers').exists():
            form_class = Supp_order_form_lf
        else:
            form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs())


class Supp_order_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppOrder.objects.get(id=self.kwargs['id'])
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_order/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Supp_order_det_create_view(CreateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.supp_order = SuppOrder.objects.get(
            id=self.kwargs["supp_order"])
        form.instance._creation_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.kwargs["supp_order"]) + "/")


class Supp_order_det_alter_view(UpdateView):
    form_class = Supp_order_det_form
    template_name = "SuppOrderDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = SuppOrderDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_order/alter/" + str(self.object.supp_order.pk) + "/")


class Supp_order_det_delete_view(DeleteView):
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


class Supp_order_view(TemplateView):
    template_name = "SuppOrder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (False):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name='supplier 100').exists():
                context['orders'] = SuppOrder.objects.all().filter(supplier_id = 1)
            elif self.request.user.groups.filter(name='supplier 200').exists():
                context['orders'] = SuppOrder.objects.all().filter(supplier_id = 2)
            elif self.request.user.groups.filter(name='supplier 300').exists():
                context['orders'] = SuppOrder.objects.all().filter(supplier_id = 3)
            else:
                context['orders'] = SuppOrder.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name='supplier 100').exists():
                context['orders'] = SuppOrder.objects.all().filter(_creation_user_id = 20)
            elif self.request.user.groups.filter(name='supplier 200').exists():
                context['orders'] = SuppOrder.objects.all().filter(_creation_user_id = 21)
            elif self.request.user.groups.filter(name='supplier 300').exists():
                context['orders'] = SuppOrder.objects.all().filter(_creation_user_id = 22)
            else:
                context['orders'] = SuppOrder.objects.all().exclude(Q(_creation_user_id = 20) | Q(_creation_user_id = 21) | Q(_creation_user_id = 22))
       
        return context
