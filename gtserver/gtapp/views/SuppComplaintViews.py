from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
#from gtapp.models import SuppOrder, SuppOrderDet
#from gtapp.forms import Supp_order_form_jg, Supp_order_form_lf, Supp_order_det_form
from gtapp.models import SuppComplaint, SuppComplaintDet, Part
from gtapp.forms import Supp_complaint_form, Supp_complaint_det_form

class Supp_complaint_create_view(CreateView):
    template_name = "SuppComplaintForm.html"
    
    def form_valid(self, form):
        form.instance._creation_user_id = self.request.user.id

        new_supp_order_complaint = form.save()
        return HttpResponseRedirect("/supp_complaint/alter/" + str(new_supp_order_complaint.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Reklamation erfassen","Bestellreklamationen")
        return context

    def get_form(self, form_class=None):
        #if self.request.user.groups.first().name == "suppliers":
        form_class = Supp_complaint_form
        #else:
        #    form_class = Supp_order_form_jg
        return form_class(**self.get_form_kwargs()) 


class Supp_complaint_alter_view(UpdateView):
    template_name = "SuppComplaintForm.html"

    def get_object(self, queryset=None):
        obj = SuppComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = SuppComplaintDet.objects.filter(supp_complaint=self.get_object().pk)
        context['supp_complaint_no'] = self.get_object().pk

        context = get_context_back(context,"Bestellreklamation ändern","Bestellreklamationen")
        return context
    
    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_complaint/")

    def get_form(self, form_class=None):
        form_class = Supp_complaint_form
        return form_class(**self.get_form_kwargs())
        
   
    

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
    template_name = "SuppComplaintForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Position erstellen","Bestellreklamationen")
        return context

    def form_valid(self, form):
        form.instance.supp_complaint = SuppComplaint.objects.get(id=self.kwargs["supp_complaint"])
        form.instance._creation_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_complaint/alter/" + str(self.kwargs["supp_complaint"]) + "/")
    
class Supp_complaint_det_alter_view(UpdateView):
    form_class = Supp_complaint_det_form
    template_name = "SuppComplaintForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context,"Bestellreklamation ändern","Bestellreklamationen")
        return context

    def get_object(self, queryset=None):
        obj = SuppComplaintDet.objects.get(id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id
        form.save()
        return HttpResponseRedirect("/supp_complaint/alter/" + str(self.object.supp_complaint.pk) + "/")

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
        context['complaints'] = SuppComplaint.objects.all()
        context = get_context_back(context,"Bestellreklamationen","Bestellreklamationen")

        return context


