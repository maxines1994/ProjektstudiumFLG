from django import forms
from django.core import validators
from django.forms import *
from gtapp.models import Article, CustOrder, CustOrderDet, Customer, Message, CustComplaint, CustComplaintDet
from gtapp.models import Part, ArtiPart, SuppOrder, SuppOrderDet, Supplier
from gtapp.models import SuppComplaint, SuppComplaintDet
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class Cust_order_form_jg(ModelForm):
    use_required_attribute = False
    class Meta:
        model = CustOrder
        fields = ["order_no", "customer", "issued_on", "delivery_date", "memo"]

class Cust_order_form_kd(ModelForm):
    use_required_attribute = False
    order_no = CharField(
        label=_('Bestellnummer'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    issued_on = IntegerField(
        label=_("Bestelltag"),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    delivery_date = IntegerField(
        label=_('Liefertag'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    
    memo = CharField(
        label=_('Kommentar'),
        required = False,
        widget=Textarea,
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )

    class Meta:
        model = CustOrder
        fields = ["order_no", "issued_on", "delivery_date", "memo"]



class Cust_order_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    unit_price = IntegerField(required=False)

    class Meta:
        model = CustOrderDet
        fields = ["pos", "article", "unit_price", "memo"]
        labels = {
            'pos': _('Positionsnummer'),
            'article': _('Artikel'),
            'unit_price': _('Stückpreis'),
            'memo': _('Kommentar'),
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }


class Cust_order_det_form_create(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    unit_price = IntegerField(required=False)

    class Meta:
        model = CustOrderDet
        fields = ["article", "unit_price", "memo"]
        labels = {
            'article': _('Artikel'),
            'unit_price': _('Stückpreis'),
            'memo': _('Kommentar'),
        }

class Msg_write_form(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Message
        fields = ["receiver", "subject", "text"]
        labels = {
            'receiver': _('Empfänger'),
            'subject': _('Betreff'),
            'text': _('Nachricht'),
        }

class Cust_complaint_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    finished_on = IntegerField(required=False)

    class Meta:
        model = CustComplaint
        fields = ["memo","finished_on"]
        labels = {
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am')
        }
        widgets = {
            #'order_no': IntegerField()
        }

class Supp_order_form_jg(ModelForm):
    use_required_attribute = False

    def __init__(self, *args, **kwargs):
        super(Supp_order_form_jg, self).__init__(*args, **kwargs)
        #HIER MUSS DER STATUS EINGEGRENZT WERDEN
        self.fields['cust_order_det'] = ChoiceField(choices=[ (o.id, str(o)+"HHAL") for o in CustOrderDet.objects.filter(cust_order__external_system=False)], label="Fertigungsauftrag")

    class Meta:
        model = SuppOrder
        fields = ["order_no","cust_order_det","issued_on","supplier","delivery_date","memo"]
        labels = {
            "order_no": _("Referenznummer"),
            "issued_on": _("Bestelldatum"),
            "supplier": _("Lieferant"),
            "delivery_date": _("Lieferdatum"),
            'memo': _('Kommentar'),
        }


class Supp_order_form_lf(ModelForm):
    use_required_attribute = False

    order_no = CharField(
        label=_('Bestellnummer'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    issued_on =  IntegerField(
        label=_("Bestelltag"),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    delivery_date =  IntegerField(
        label=_('Liefertag'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )

    memo = CharField(
        label=_('Kommentar'),
        required = False,
        widget=Textarea,
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )

    class Meta:
        model = SuppOrder
        fields = ["order_no","issued_on","delivery_date","memo"]
        labels = {
            'memo': _('Kommentar'),
        }


class Supp_order_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    unit_price = IntegerField(required=False)

    class Meta:
        model = SuppOrderDet
        fields = ["pos","part","quantity","unit_price","memo"]
        labels = {
            'pos': _('Positionsnummer'),
            'part': _('Artikel'),
            'quantity': _('Menge'),
            'unit_price': _('Preis'),
            'memo': _('Kommentar'),
        }


class Supp_complaint_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    finished_on = IntegerField(required=False)

    class Meta:
        model = SuppComplaint
        fields = ["memo", "finished_on"]
        labels = {
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am')
        }
        widgets = {
            #'order_no': IntegerField()
        }

class Cust_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)

    class Meta:
        model = CustComplaintDet
        fields = ["pos","cust_order_det","memo","quantity"]
        labels = {
            'pos': _('Position'),
            'cust_oder_det': _('Position'),
            'memo': _('Kommentar'),
            'quantity': _('Anzahl')
        }

class Supp_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    finished_on = IntegerField(required=False)

    class Meta:
        model = SuppComplaintDet
        fields = ["supp_order","supp_order_det","memo", "finished_on"]
        labels = {
            'supp_order': _("Bestellung"),
            'supp_oder_det': _('Position'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am'),            
        }
        widgets = {
            #'order_no': IntegerField()
        }
