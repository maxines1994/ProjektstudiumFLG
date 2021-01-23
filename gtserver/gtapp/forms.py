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
        fields = ["order_no", "customer", "issued_on",
                  "delivery_date", "memo"]

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
    
    order_no = CharField(
        label=_('Bestellnummer'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    supplier = ModelChoiceField(
        Supplier.objects.filter(pk__gt=0),
        label=_('Kunde'),
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
        fields = ["order_no","issued_on","supplier","delivery_date","memo"]
        labels = {
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
        fields = ["supplier","supp_order","memo", "finished_on"]
        labels = {
            'supplier': _("Lieferant"),
            'supp_order': _('Bestellung'),
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
        fields = ["supp_order_det","memo", "finished_on"]
        labels = {
            'supp_oder_det': _('Position'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am'),            
        }
        widgets = {
            #'order_no': IntegerField()
        }

    def __init__(self, supp_order_id, *args, **kwargs):
        super(Supp_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['supp_order_det'].queryset = SuppOrderDet.objects.filter(supp_order_id= supp_order_id)
