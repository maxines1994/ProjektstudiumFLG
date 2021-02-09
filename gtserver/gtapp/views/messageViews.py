from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from gtapp.forms import Cust_order_form_jg, Cust_order_form_kd, Cust_order_det_form, Cust_order_det_form_create, Msg_write_form
from gtapp.models import MessageUser, Message, Timers, CustOrder, CustOrderDet, SuppOrder, SuppOrderDet
from django.contrib.auth.models import Group, User
import json
from gtapp.constants import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class inboxView(LoginRequiredMixin, TemplateView):
    template_name = "inbox.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Posteingang", "")
        context["msg"] = MessageUser.objects.filter(
            is_trash=False, user=self.request.user, user_is_sender=False)
        context["p"] = "in"
        return context


class outboxView(LoginRequiredMixin, TemplateView):
    template_name = "inbox.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Postausgang", "")
        context["msg"] = MessageUser.objects.filter(
            user=self.request.user, user_is_sender=True)
        context["p"] = "out"
        return context


class binView(LoginRequiredMixin, TemplateView):
    template_name = "inbox.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Papierkorb", "")
        context["msg"] = MessageUser.objects.filter(
            is_trash=True, user=self.request.user, user_is_sender=False)
        context["p"] = "bin"
        return context


class msgWriteView(LoginRequiredMixin, CreateView):
    template_name = "message.html"
    form_class = Msg_write_form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Nachricht", "")

        # Orders zum anhängen, nur die des benutzers
        if self.request.user.groups.filter(name=L100).exists():
            context['orders'] = SuppOrder.objects.filter(supplier_id=1, external_system=True)
        elif self.request.user.groups.filter(name=L200).exists():
            context['orders'] = SuppOrder.objects.filter(supplier_id=2, external_system=True)
        elif self.request.user.groups.filter(name=L300).exists():
            context['orders'] = SuppOrder.objects.filter(supplier_id=3, external_system=True)
        elif self.request.user.groups.filter(name=JOGA).exists():
            context['orders'] = SuppOrder.objects.filter(external_system=False)

        return context

    # Umleitung auf die Alter View
    def form_valid(self, form):
        form.instance.sent_on = Timers.get_current_day()
        form.instance.sender = self.request.user
        newmessage = form.save()

        for i in form.instance.receiver.user_set.all():
            print(i)
            MessageUser.objects.create(user=i, user_is_sender=False, message=newmessage, is_trash=False)
        
        MessageUser.objects.create(
            user=form.instance.sender, user_is_sender=True, message=newmessage, is_trash=False)
        return HttpResponseRedirect(reverse("inbox"))

class msgDetailsView(LoginRequiredMixin, DetailView):
    template_name = "message_detail.html"
    model = Message


    def get_object(self, queryset=None):
        mu = MessageUser.objects.filter(pk=self.kwargs['id'])[0]
        obj = Message.objects.get(pk=mu.message.pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Nachricht", "")
        return context

# Weise Task User zu

@login_required
def delete_message_view(request, **kwargs):
    if MessageUser.objects.filter(pk=kwargs["id"], user=request.user, user_is_sender=False)[0].is_trash == False:
        MessageUser.objects.filter(pk=kwargs["id"], user=request.user, user_is_sender=False).update(is_trash=True)
    else:
        MessageUser.objects.filter(pk=kwargs["id"], user=request.user, user_is_sender=False).update(is_trash=False)
    return HttpResponseRedirect(reverse("inbox"))


@login_required
def add_order_view(request, **kwargs):
    o = SuppOrder.objects.filter(pk=kwargs["id"])[0]
    order = {
        "customer": o.supplier.name,
        "no": o.order_no,
        "issued": o.issued_on,
        "posl": SuppOrderDet.objects.filter(supp_order=kwargs["id"]).count(),
    }
    s=0
    for i in SuppOrderDet.objects.filter(supp_order=kwargs["id"]):
        s = s+1
        pos = {
            "article": i.part.description,
            "posno": i.pos,
            "quantity": i.quantity
        }
        order[s] = pos
    return HttpResponse(json.dumps(order))
