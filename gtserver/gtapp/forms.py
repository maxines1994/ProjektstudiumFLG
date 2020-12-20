from django import forms
from django.core import validators
from django.forms import *
from gtapp.models import Article, CustOrder, CustOrderDet, Customer
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class Cust_order_form(ModelForm):
    use_required_attribute = False
    order_no = CharField(
        label=_('Bestellnummer'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    costumer = ModelChoiceField(
        Customer.objects.filter(pk__gt=0),
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
    price = IntegerField(
        label=_('Preis'),
        error_messages={
            'required': "Dieses Feld ist ein Pflichtfeld!",
            'invalid': "Dieses Feld wurde nicht korrekt ausgefüllt!"
        }
    )
    class Meta:
        model = CustOrder
        fields = ["order_no","costumer","issued_on","delivery_date","price","memo"]
        labels = {
            'memo': _('Kommentar'),
        }

    

class Cust_order_det_form(ModelForm):
    use_required_attribute = False
    class Meta:
        model = CustOrderDet
        fields = ["pos","article","unit_price","memo"]
        labels = {
            'pos': _('Positionsnummer'),
            'article': _('Artikel'),
            'unit_price': _('Stückpreis'),
            'memo': _('Kommentar'),
        }

