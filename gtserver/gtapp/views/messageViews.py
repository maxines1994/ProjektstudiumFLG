from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, FormView, DetailView
from gtapp.forms import Cust_order_form_jg, Cust_order_form_kd, Cust_order_det_form, Cust_order_det_form_create, Msg_write_form
from gtapp.models import *
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
        context["action"] = "inbox"
        return context


class outboxView(LoginRequiredMixin, TemplateView):
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Postausgang", "")
        context["msg"] = MessageUser.objects.filter(
            user=self.request.user, user_is_sender=True)
        context["action"] = "outbox"
        return context


class binView(LoginRequiredMixin, TemplateView):
    template_name = "inbox.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Papierkorb", "")
        context["msg"] = MessageUser.objects.filter(
            is_trash=True, user=self.request.user, user_is_sender=False)
        context["action"] = "bin"
        return context


class msgWriteView(LoginRequiredMixin, CreateView):
    template_name = "message.html"
    form_class = Msg_write_form

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(msgWriteView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        # Vorbelegung Empfänger für Lieferanten und Kunden
        if self.request.user.groups.filter(name=KUNDEN).exists():
            return {'receiver': Group.objects.get(name=KUNDENDIENST)}
        elif self.request.user.groups.filter(name=LIEFERANTEN).exists():
            return {'receiver': Group.objects.get(name=PRODUKTIONSDIENSTLEISTUNG)}
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_context_back(context, "Nachricht", "")
        # Alle Dokumente die der User anhängen kann, je nach Usergruppe
        if self.request.user.groups.filter(name=L100).exists():
            context['supporders'] = SuppOrder.objects.filter(supplier_id=1, external_system=True, pk__gt=6)
            context['suppcomplaints'] = SuppComplaint.objects.filter(supplier_id=1, external_system=True)
        elif self.request.user.groups.filter(name=L200).exists():
            context['supporders'] = SuppOrder.objects.filter(supplier_id=2, external_system=True, pk__gt=6)
            context['suppcomplaints'] = SuppComplaint.objects.filter(supplier_id=2, external_system=True)
        elif self.request.user.groups.filter(name=L300).exists():
            context['supporders'] = SuppOrder.objects.filter(supplier_id=3, external_system=True, pk__gt=6)
            context['suppcomplaints'] = SuppComplaint.objects.filter(supplier_id=3, external_system=True)
        elif self.request.user.groups.filter(name=K1).exists():
            context['custorders'] = CustOrder.objects.filter(customer_id=1, external_system=True)
            context['custcomplaints'] = CustComplaint.objects.filter(customer_id=1, external_system=True)
        elif self.request.user.groups.filter(name=K2).exists():
            context['custorders'] = CustOrder.objects.filter(customer_id=2, external_system=True)
            context['custcomplaints'] = CustComplaint.objects.filter(customer_id=2, external_system=True)
        elif self.request.user.groups.filter(name=K3).exists():
            context['custorders'] = CustOrder.objects.filter(customer_id=3, external_system=True)
            context['custcomplaints'] = CustComplaint.objects.filter(customer_id=3, external_system=True)
        elif self.request.user.groups.filter(name=JOGA).exists():
            context['supporders'] = SuppOrder.objects.filter(external_system=False, pk__gt=6)
            context['custorders'] = CustOrder.objects.filter(external_system=False)
            context['suppcomplaints'] = SuppComplaint.objects.filter(external_system=False)
            context['custcomplaints'] = CustComplaint.objects.filter(external_system=False)
        return context

    # Umleitung auf die Alter View
    def form_valid(self, form):
        print("Test")
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

     

        obj = self.get_object()
        if obj.sender == self.request.user:
            context["is_sender"] = True
        else:
            obj.read_by_group = True
            obj.save()
            context["is_sender"] = False
        
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
    # Beziehen des übergeordneten Models und des untergeordneten Details-Models
    main_model = GtModel.str_to_gtmodel(kwargs['model'])
    det_model = GtModel.str_to_gtmodel(kwargs['model']+"Det")

    # Setzen des Filters mit dynamischen Feldnamen zu den beiden Models
    myfilter={}
    myfilter[get_fieldname(model=det_model,foreign_key_model=main_model)] = kwargs["id"]

    # Beziehen der übergeordneten Instanz und der untergeordneten Instanzen
    main = main_model.objects.get(pk=kwargs['id'])
    alldets = det_model.objects.filter(**myfilter)

    # Ausgeben der übergeordneten Intanz als Dictionary
    order = {
        "no": "Bestellnummer: " + str(main.order_no),
        "issued": "Angelegt am: " + str(main.issued_on),
        "posl": "Positionsanzahl: " + str(alldets.count()),
        "memo": "Kommentar: " + str(main.memo)
    }

    # Variables füllen der übergeordneten Instanz als Dictionary variabel nach Cust oder (else) Supp
    if CustOrder.__instancecheck__(main):
        order['partner'] = "Partner: " + str(main.customer.name)
        order['deliverydate'] = "Lieferdatum: " + str(main.delivery_date)
    elif SuppOrder.__instancecheck__(main):
        order['partner'] = "Partner: " + str(main.supplier.name)
        order['deliverydate'] = "Lieferdatum: " + str(main.delivery_date)
    elif CustComplaint.__instancecheck__(main):
        order['partner'] = "Partner: " + str(main.cust_order.customer.name)
    elif SuppComplaint.__instancecheck__(main):
        order['partner'] = "Partner: " + str(main.supp_order.supplier.name)
    else:
        order['partner'] = "-"

    bx = str(main.box_no) if main.box_no is not None else ""
    order['Boxnummer'] = "Boxnummer: " + bx

    # Füllen der untergeordneten Instanzen in das Dictionary
    s=0
    for i in alldets:
        s = s+1
        pos = {}
        # Variables füllen der untergeordneten Instanzen je nach Cust oder (else) Supp
        if CustOrderDet.__instancecheck__(i):
            pos["particle"] = "Produkt: " + str(i.article.description)
        elif CustComplaintDet.__instancecheck__(i):
            pos["particle"] = "Produkt: " + str(i.cust_order_det.article.description)
        elif SuppOrderDet.__instancecheck__(i):
            pos["particle"] = "Produkt: " + str(i.part.description)
            pos["quantity"] = "Menge: " + str(i.quantity)
        elif SuppComplaintDet.__instancecheck__(i):
            pos["particle"] = "Produkt: " + str(i.supp_order_det.part.description)
            pos["quantity"] = "Menge: " + str(i.quantity)
            pos["newdelivery"] = "Neulieferung erforderlich" if i.redelivery else "Neulieferung nicht erforderlich"
        else:
            pos["particle"] = "-"
        
        pos["memo"] = "Kommentar: " + str(i.memo)
        bx = str(i.box_no) if i.box_no is not None else ""
        pos["box_no"] = "Boxnummer: " + bx

        # Einfügen der untergeordneten gefüllten Positionen in den Aufragskopf bzw. die übergeordnete Instanz
        pos['posno'] = "Positionsnummer: " + str(i.pos)
        order[s] = pos
    # Return als JSON
    return HttpResponse(json.dumps(order))

def get_fieldname(model: GtModel, foreign_key_model: GtModel):
    """
    Diese Funktion sucht die richtige Feldbezeichnung des Fremdschluessels  in der Tabelle "model" 
    anhand des übergebenen Models des Fremdschluessels "foreign_key_model".
    Die Feldbezeichnungen der Fremdschlussel in den Models entsprechen nicht den Namen
    der verknuepften Models. Deshalb wird anhand des Modelnamens das entsprechende Feld gesucht.
    Beispiel:
    In der SuppOrderDet gibt es das Feld "supp_order". Wenn als model "SuppOrderDet" und als
    foreign_key_model "SuppOrder" uebergeben werden, gibt diese Funktion "supp_order" zurück.
    """
    for item in model._meta.fields:
        if item.name.replace("_","") == foreign_key_model.__name__.casefold():
            return str(item.name)
