from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView
from gtapp.models import SuppComplaint, SuppComplaintDet, Part, SuppOrder, Task, Timers, Stock, SuppOrderDet
from gtapp.forms import Supp_complaint_form, Supp_complaint_form_kanban, Supp_complaint_det_form
from django import forms
from gtapp.models import LiveSettings
from gtapp.constants import *
from django.contrib.auth.mixins import LoginRequiredMixin

class Supp_complaint_create_view(LoginRequiredMixin, CreateView):
    template_name = "SuppComplaintForm.html"
    
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

        new_supp_order_complaint = form.save()

        if form.instance.external_system == True:
            if self.request.user.groups.filter(name=L100).exists():
                Task.set_task(new_supp_order_complaint, 40)
            elif self.request.user.groups.filter(name=L200).exists():
                Task.set_task(new_supp_order_complaint, 41)
            elif self.request.user.groups.filter(name=L300).exists():
                Task.set_task(new_supp_order_complaint, 42)
        else:
            if self.request.user.groups.filter(name=PRODUKTION).exists():
                Task.set_task(new_supp_order_complaint, 32)
            elif self.request.user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists(): 
                Task.set_task(new_supp_order_complaint, 43)

        return HttpResponseRedirect("/supp_complaint/alter/" + str(new_supp_order_complaint.pk) + "/")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name__in=[L100, L200]).exists():
            form_class = Supp_complaint_form_kanban
        else:
            form_class = Supp_complaint_form
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_create_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        kwargs.update({'user_groups': self.request.user.groups.all() })

        return kwargs

    def get_initial(self):
        if self.request.user.groups.filter(name=L100).exists():
            suppliers = [1]
        elif self.request.user.groups.filter(name=L200).exists():
            suppliers = [2]
        elif self.request.user.groups.filter(name=L300).exists():
            suppliers = [3]
        else:
            suppliers = [1, 2, 3]

        if len(suppliers) == 1:
            supp_order = SuppOrder.objects.filter(supplier__in=suppliers, external_system=True).order_by('_creation_date').first()
        else:
            supp_order = SuppOrder.objects.filter(supplier__in=suppliers, external_system=False).order_by('_creation_date').first()

        return {'supp_order': supp_order}


class Supp_complaint_alter_view(LoginRequiredMixin, UpdateView):
    template_name = "SuppComplaintForm.html"

    def get_object(self, queryset=None):
        obj = SuppComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = SuppComplaintDet.objects.filter(supp_complaint=self.get_object().pk)
        context['supp_complaint_no'] = self.get_object().pk
        context["action"] = "alter"

        context['POS_STATUS'] = SuppComplaintDet.Status.__members__
        context['OBJ_STATUS'] = self.get_object().status
        context['STATUS'] = SuppComplaint.Status.__members__
        context['object'] = self.get_object()

        context['button_neubestellung'] = SuppComplaintDet.objects.filter(supp_complaint=self.get_object(),status=SuppComplaintDet.Status.NEU_BESTELLEN).exists()
        #context['button_abschliessen'] = not SuppComplaintDet.objects.filter(supp_complaint=self.get_object(),status__lte=10).exists()

        
        # Nur bei BoxScan implementieren? vv
        # context['redelivery'] = SuppComplaintDet.objects.filter(supp_complaint=self.get_object().pk,redelivery=True).exists()

        # Durchlaufe alle items und pruefe fuer jeden, ob genug Bestand da ist.
        # Schreibe fuer jedes item einen entsprechenden boolschen Wert in eine Liste
        
        has_enough_stock_list = []
        for item in context['items']:
            my_part = Part.objects.get(id=SuppOrderDet.objects.get(id=item.supp_order_det_id).part_id)
            my_stock = Stock.objects.get(is_supplier_stock=False, part=my_part)
            has_enough_stock = my_stock.stock - my_stock.reserved >= item.quantity
            has_enough_stock_list.append(has_enough_stock)

        context['has_enough_stock'] = has_enough_stock_list

        context['items_has_enough_stock'] = zip(context['items'], context['has_enough_stock'])
        
        #Trigger Pos update -> Not sure how smart that actually is tbh
        try:
            SuppComplaintDet.objects.filter(supp_complaint=self.get_object()).first().postsave()
        except: 
            pass
        # @Bash Ich habe die Funktionalität in die Methode postsave() ausgelagert, die jetzt auch korrekterweise nach dem Speichern feuert.
        # Btw, update() triggert leider nix, ist wie ein SQL-Statement (Django-Limitation). Aber set_status() aus StatusViews.py und auch ein direktes .save() funktioniert.

        return context
    
    def form_valid(self, form):
        form.instance._update_user_id = self.request.user.id

        form.save()
        return HttpResponseRedirect("/supp_complaint/")

    def get_form(self, form_class=None):
        if self.request.user.groups.filter(name__in=[L100, L200]).exists():
            form_class = Supp_complaint_form_kanban
        else:
            form_class = Supp_complaint_form
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(Supp_complaint_alter_view, self).get_form_kwargs()

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        kwargs.update({'user_groups': self.request.user.groups.all() })
        return kwargs

        
class Supp_complaint_delete_view(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppComplaint.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_complaint/"
        self.object.delete()
        return HttpResponseRedirect(success_url)

class Supp_complaint_det_create_view(LoginRequiredMixin, CreateView):
    form_class = Supp_complaint_det_form
    template_name = "SuppComplaintDetForm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "create"
        return context

    def form_valid(self, form):
        form.instance.supp_complaint = SuppComplaint.objects.get(id=self.kwargs["supp_complaint"])
        form.instance._creation_user_id = self.request.user.id

        # Position vergeben
        try:
            form.instance.pos = SuppComplaintDet.objects.filter(supp_complaint=form.instance.supp_complaint).latest('_creation_date').pos + 1
        except SuppComplaintDet.DoesNotExist:
            form.instance.pos = 1

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


class Supp_complaint_det_alter_view(LoginRequiredMixin, UpdateView):
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

class Supp_complaint_det_delete_view(LoginRequiredMixin, DeleteView):
    template_name = "delete.html"

    def get_object(self, queryset=None):
        obj = SuppComplaintDet.objects.get(id=self.kwargs['id'])
        return obj
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = "/supp_complaint/alter/" + str(self.object.supp_complaint.pk) + "/"
        self.object.delete()
        return HttpResponseRedirect(success_url)
    
class Supp_complaint_view(LoginRequiredMixin, TemplateView):
    template_name = "SuppComplaint.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["STATUS"] = SuppComplaint.Status.__members__
        context["POS_STATUS"] = SuppComplaintDet.Status.__members__

        if (LiveSettings.objects.all().first().phase_3):
            # 3. Digitalisierungsstufe
            if self.request.user.groups.filter(name=L100).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 1))
            elif self.request.user.groups.filter(name=L200).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 2))
            elif self.request.user.groups.filter(name=L300).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 3))
            else:
                context['complaints'] = SuppComplaint.objects.all()
        else:
            # 2. Digitalisierungsstufe
            if self.request.user.groups.filter(name=L100).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 1, external_system=True))
            elif self.request.user.groups.filter(name=L200).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 2, external_system=True))
            elif self.request.user.groups.filter(name=L300).exists():
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(supplier_id = 3, external_system=True))
            else:
                context['complaints'] = SuppComplaint.objects.all().filter(supp_order__in = SuppOrder.objects.all().filter(external_system=False))
       
        return context
