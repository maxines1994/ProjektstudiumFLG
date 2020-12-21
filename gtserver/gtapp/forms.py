from django import forms
from django.forms import *
from gtapp.models import Article, CustOrder, CustOrderDet, Customer
from gtapp.models import Part, ArtiPart, SuppOrder, SuppOrderDet, Supplier
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


class Supp_order_form(ModelForm):
    class Meta:
        model = SuppOrder
        fields = ["order_no","issued_on","supplier","delivery_date","memo"]
        labels = {
            'order_no': _('Nummer'),
            'issued_on': _('Bestelltag'),
            'supplier': _("Lieferant"),
            'delivery_date': _('Liefertag'),
            'memo': _('Kommentar'),
        }
        widgets = {
            #'order_no': IntegerField()
        }
        # -> Boxnummer

    #Prüft vor der Initialisierung den user und die Usergroups
    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups', None)
        user_name = kwargs.pop('user_name', None)
        super(Supp_order_form, self).__init__(*args, **kwargs)

        if groups == "suppliers":
            self.fields['supplier'].widget = HiddenInput()
            self.fields['supplier'].initial = user_name[3]

class Supp_order_det_form(ModelForm):
    class Meta:
        model = SuppOrderDet
        fields = ["pos","part","quantity","unit_price","memo"] #"pack_quantity", 
        labels = {
            'pos': _('Positionsnummer'),
            'part': _('Artikel'),
            #'pack_quantity': _('Strukturmenge'),
            'quantity': _('Bestellmenge'),
            'unit_price': _('price'),
            'memo': _('Kommentar'),
        }
