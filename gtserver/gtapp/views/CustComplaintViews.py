from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import CustComplaint, CustComplaintDet, Article
from gtapp.forms import Cust_complaint_form, Cust_complaint_det_form

class Cust_complaint_create_view(CreateView):
    template_name = "CustComplaintForm.html"
    
    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id

        new_cust_order_complaint = form.save()
        return HttpResponseRedirect("/cust_complaint/alter/" + str(new_cust_order_complaint.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        #if self.request.user.groups.first().name == "suppliers":
        form_class = Cust_complaint_form
        #else:
        #    form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs()) 

class Cust_complaint_alter_view(UpdateView):
    template_name = "CustComplaintForm.html"

    def get_object(self, queryset=None):
        obj = CustComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = CustComplaintDet.objects.filter(cust_complaint=self.get_object().pk)
        context['cust_complaint_no'] = self.get_object().pk
        context["action"] = "alter"
        return context
    
    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/cust_complaint/")

    def get_form(self, form_class=None):
        form_class = Cust_complaint_form
        return form_class(**self.get_form_kwargs())
        
class Cust_complaint_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = CustComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/cust_complaint/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Cust_complaint_det_create_view(CreateView):
    form_class = Cust_complaint_det_form
    template_name = "CustComplaintDetForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.cust_complaint = CustComplaint.objects.get(id=self.kwargs["cust_complaint"])
        form.instance._creation_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/cust_complaint/alter/" + str(self.kwargs["cust_complaint"]) + "/")
    
class Cust_complaint_det_alter_view(UpdateView):
    form_class = Cust_complaint_det_form
    template_name = "CustComplaintDetForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "alter"
        return context

    def get_object(self, queryset=None):
        obj = CustComplaintDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/cust_complaint/alter/" + str(self.object.cust_complaint.pk) + "/")

class Cust_complaint_det_delete_view(DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = CustComplaintDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/cust_complaint/alter/" + str(self.object.cust_complaint.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
class Cust_complaint_view(TemplateView):
    template_name = "CustComplaint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['complaints'] = CustComplaint.objects.all()
        return context