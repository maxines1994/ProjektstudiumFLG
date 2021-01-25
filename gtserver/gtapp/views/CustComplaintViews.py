from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import CustComplaint, CustComplaintDet, Article, CustOrder, CustOrderDet
from gtapp.forms import Cust_complaint_form, Cust_complaint_det_form
from django.db.models import Q

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

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Cust_complaint_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        if (False):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                customers = [1]
            elif self.request.user.groups.filter(name='customer 2').exists():
                customers = [2]
            elif self.request.user.groups.filter(name='customer 3').exists():
                customers = [3]
            else:
                customers = [1,2,3]
            kwargs.update({'customers': customers})
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                user = 5
            elif self.request.user.groups.filter(name='customer 2').exists():
                user = 6
            elif self.request.user.groups.filter(name='customer 3').exists():
                user = 7
            else:
                user = 0
            kwargs.update({'user': user})
        
        return kwargs


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

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Cust_complaint_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        if (False):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                customers = [1]
            elif self.request.user.groups.filter(name='customer 2').exists():
                customers = [2]
            elif self.request.user.groups.filter(name='customer 3').exists():
                customers = [3]
            else:
                customers = [1,2,3]
            kwargs.update({'customers': customers})
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                user = 5
            elif self.request.user.groups.filter(name='customer 2').exists():
                user = 6
            elif self.request.user.groups.filter(name='customer 3').exists():
                user = 7
            else:
                user = 0
            kwargs.update({'user': user})
        
        return kwargs
    
        
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

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Cust_complaint_det_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        kwargs.update({'cust_order_id': CustComplaint.objects.get(pk=self.kwargs['cust_complaint']).cust_order.id})
        return kwargs

    
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

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Cust_complaint_det_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        cust_complaint_id = CustComplaintDet.objects.get(pk=self.kwargs['id']).cust_complaint.id
        kwargs.update({'cust_order_id': CustComplaint.objects.get(pk=cust_complaint_id).cust_order.id})
        return kwargs


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

        if (False):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                context['complaints'] = CustComplaint.objects.all().filter(cust_order__in = CustOrder.objects.all().filter(customer_id = 1))
            elif self.request.user.groups.filter(name='customer 2').exists():
                context['complaints'] = CustComplaint.objects.all().filter(cust_order__in = CustOrder.objects.all().filter(customer_id = 2))
            elif self.request.user.groups.filter(name='customer 3').exists():
                context['complaints'] = CustComplaint.objects.all().filter(cust_order__in = CustOrder.objects.all().filter(customer_id = 3))
            else:
                context['complaints'] = CustComplaint.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name='customer 1').exists():
                context['complaints'] = CustComplaint.objects.all().filter(_creation_user_id = 5)
            elif self.request.user.groups.filter(name='customer 2').exists():
                context['complaints'] = CustComplaint.objects.all().filter(_creation_user_id = 6)
            elif self.request.user.groups.filter(name='customer 3').exists():
                context['complaints'] = CustComplaint.objects.all().filter(_creation_user_id = 7)
            else:
                context['complaints'] = CustComplaint.objects.all().exclude(Q(_creation_user_id = 5) | Q(_creation_user_id = 6) | Q(_creation_user_id = 7))
       
        return context
