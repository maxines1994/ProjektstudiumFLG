from django import forms
from django.forms import *
from gtapp.models import Article, CustOrder, CustOrderDet, Customer
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class Cust_order_form(ModelForm):
    class Meta:
        model = CustOrder
        fields = ["order_no","costumer","issued_on","delivery_date","price","memo"]
        labels = {
            'order_no': _('Bestellnummer'),
            'costumer': _('Kunde'),
            'issued_on': _('Bestelltag'),
            'delivery_date': _('Liefertag'),
            'price': _('Preis'),
            'memo': _('Kommentar'),
        }
        widgets = {
            #'order_no': IntegerField()
        }
    

class Cust_order_det_form(ModelForm):
    class Meta:
        model = CustOrderDet
        fields = ["pos","article","unit_price","memo"]
        labels = {
            'pos': _('Positionsnummer'),
            'article': _('Artikel'),
            'unit_price': _('Stückpreis'),
            'memo': _('Kommentar'),
        }
