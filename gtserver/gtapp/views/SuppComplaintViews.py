from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import SuppComplaint, SuppComplaintDet, Part, SuppOrder
from gtapp.forms import Supp_complaint_form, Supp_complaint_det_form
from django import forms
from gtapp.models import LiveSettings


class Supp_complaint_create_view(CreateView):
    template_name = "SuppComplaintForm.html"
    
    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id
        
        if self.request.user.groups.filter(name='supplier 100').exists():
            form.instance.supplier_id = 1
        elif self.request.user.groups.filter(name='supplier 200').exists():
            form.instance.supplier_id = 2
        elif self.request.user.groups.filter(name='supplier 300').exists():
            form.instance.supplier_id = 3
        
        if self.request.user.groups.filter(name='suppliers').exists():
            form.instance.external_system = True

        new_supp_order_complaint = form.save()

        return HttpResponseRedirect("/supp_complaint/alter/" + str(new_supp_order_complaint.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        #if self.request.user.groups.first().name == "suppliers":
        form_class = Supp_complaint_form
        #else:
        #    form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        if self.request.user.groups.filter(name='supplier 100').exists():
            suppliers = [1]
        elif self.request.user.groups.filter(name='supplier 200').exists():
            suppliers = [2]
        elif self.request.user.groups.filter(name='supplier 300').exists():
            suppliers = [3]
        else:
            suppliers = [1,2,3]
        kwargs.update({'suppliers': suppliers})
        return kwargs


class Supp_complaint_alter_view(UpdateView):
    template_name = "SuppComplaintForm.html"

    def get_object(self, queryset=None):
        obj = SuppComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = SuppComplaintDet.objects.filter(supp_complaint=self.get_object().pk)
        context['supp_complaint_no'] = self.get_object().pk
        context["action"] = "alter"
        return context
    
    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id

        form.save()
        return HttpResponseRedirect("/supp_complaint/")

    def get_form(self, form_class=None):
        form_class = Supp_complaint_form
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        if self.request.user.groups.filter(name='supplier 100').exists():
            suppliers = [1]
        elif self.request.user.groups.filter(name='supplier 200').exists():
            suppliers = [2]
        elif self.request.user.groups.filter(name='supplier 300').exists():
            suppliers = [3]
        else:
            suppliers = [1,2,3]
        kwargs.update({'suppliers': suppliers})
        return kwargs

        
class Supp_complaint_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_complaint/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Supp_complaint_det_create_view(CreateView):
    form_class = Supp_complaint_det_form
    template_name = "SuppComplaintDetForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.supp_complaint = SuppComplaint.objects.get(id=self.kwargs["supp_complaint"])
        form.instance._creation_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_complaint/alter/" + str(self.kwargs["supp_complaint"]) + "/")

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_det_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        kwargs.update({'supp_order_id': SuppComplaint.objects.get(pk=self.kwargs['supp_complaint']).supp_order.id})
        return kwargs


class Supp_complaint_det_alter_view(UpdateView):
    form_class = Supp_complaint_det_form
    template_name = "SuppComplaintDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = SuppComplaintDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_complaint/alter/" + str(self.object.supp_complaint.pk) + "/")
    
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_det_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        supp_complaint_id = SuppComplaintDet.objects.get(pk=self.kwargs['id']).supp_complaint.id
        kwargs.update({'supp_order_id': SuppComplaint.objects.get(pk=supp_complaint_id).supp_order.id})
        return kwargs

class Supp_complaint_det_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppComplaintDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_complaint/alter/" + str(self.object.supp_complaint.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
class Supp_complaint_view(TemplateView):
    template_name = "SuppComplaint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (LiveSettings.objects.all().first().phase_3):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name='supplier 100').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 1))
            elif self.request.user.groups.filter(name='supplier 200').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 2))
            elif self.request.user.groups.filter(name='supplier 300').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 3))
            else:
                context['complaints'] = SuppComplaint.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name='supplier 100').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 1, external_system=True))
            elif self.request.user.groups.filter(name='supplier 200').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 2, external_system=True))
            elif self.request.user.groups.filter(name='supplier 300').exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 3, external_system=True))
            else:
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(external_system=False))
       
        return context
