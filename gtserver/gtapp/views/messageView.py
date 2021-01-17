from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from gtapp.forms import Cust_order_form, Cust_order_det_form, Cust_order_det_form_create, Msg_write_form
from gtapp.models import MessageUser, Message, Timers, CustOrder, CustOrderDet
from django.contrib.auth.models import Group, User
import json


class inboxView(TemplateView):
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Posteingang", "")
        context["msg"] = MessageUser.objects.filter(
            is_trash=False, user=self.request.user, user_is_sender=False)
        context["p"] = "in"
        return context


class outboxView(TemplateView):
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Postausgang", "")
        context["msg"] = MessageUser.objects.filter(
            user=self.request.user, user_is_sender=True)
        context["p"] = "out"
        return context


class binView(TemplateView):
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Papierkorb", "")
        context["msg"] = MessageUser.objects.filter(
            is_trash=True, user=self.request.user, user_is_sender=False)
        context["p"] = "bin"
        return context


class msgWriteView(CreateView):
    template_name = "message.html"
    form_class = Msg_write_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Nachricht", "")

        # Orders zum anhängen, nur die des benutzers
        if self.request.user.groups.filter(name='customer 1').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=1)
        elif self.request.user.groups.filter(name='customer 2').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=2)
        elif self.request.user.groups.filter(name='customer 3').exists():
            context['orders'] = CustOrder.objects.filter(customer_id=3)
        elif self.request.user.groups.filter(name='JOGA').exists():
            context['orders'] = CustOrder.objects.all()

        return context

    # Umleitung auf die Alter View
    def form_valid(self, form):
        form.instance.sent_on = Timers.get_current_day()
        form.instance.sender = self.request.user
        newmessage = form.save()
        for i in User.objects.filter(groups=form.instance.receiver):
            MessageUser.objects.create(
                user=i, user_is_sender=False, message=newmessage, is_trash=False)
        MessageUser.objects.create(
            user=form.instance.sender, user_is_sender=True, message=newmessage, is_trash=False)
        return HttpResponseRedirect(reverse("inbox"))


class msgDetailsView(DetailView):
    template_name = "message_detail.html"
    model = Message

    def get_object(self, queryset=None):
        mu = MessageUser.objects.filter(self.kwargs['id'])[0]
        obj = Message.objects.get(pk=mu.message.pk)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Nachricht", "")
        return context

# Weise Task User zu


def delete_message_view(request, **kwargs):
    if MessageUser.objects.filter(message_id=kwargs["id"], user=request.user, user_is_sender=False)[0].is_trash == False:
        MessageUser.objects.filter(
            message_id=kwargs["id"], user=request.user, user_is_sender=False).update(is_trash=True)
    else:
        MessageUser.objects.filter(
            message_id=kwargs["id"], user=request.user, user_is_sender=False).update(is_trash=False)
    return HttpResponseRedirect(reverse("inbox"))


def add_order_view(request, **kwargs):
    o = CustOrder.objects.filter(pk=kwargs["id"])[0]
    order = {
        "customer": o.customer.name,
        "no": o.pk,
        "issued": o.issued_on,
        "posl": CustOrderDet.objects.filter(cust_order=kwargs["id"]).count(),
    }
    s=0
    for i in CustOrderDet.objects.filter(cust_order=kwargs["id"]):
        s = s+1
        pos = {
            "article": i.article.description,
            "price": i.unit_price,
            "posno": i.pos
        }
        order[s] = pos
    return HttpResponse(json.dumps(order))
