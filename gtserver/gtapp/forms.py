from django import forms
from django.core import validators
from django.forms import *
from gtapp.models import Article, CustOrder, CustOrderDet, Customer, Message, CustComplaint, CustComplaintDet
from gtapp.models import Part, ArtiPart, SuppOrder, SuppOrderDet, Supplier
from gtapp.models import SuppComplaint, SuppComplaintDet
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


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
        fields = ["cust_order","memo","finished_on"]
        labels = {
            'cust_order': _('Auftrag'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am')
        }
        widgets = {
            #'order_no': IntegerField()
        }

    if (True):
        # 3. Digitalisierungsstufe
        def __init__(self, customers, *args, **kwargs):
            super(Cust_complaint_form, self).__init__(*args, **kwargs)
            self.fields['cust_order'].queryset = CustOrder.objects.filter(customer__in=customers)
    else:
        # 2. Digitalisierungsstufe
        def __init__(self, user, *args, **kwargs):
            super(Cust_complaint_form, self).__init__(*args, **kwargs)
            if user != 0:
                self.fields['cust_order'].queryset = CustOrder.objects.filter(_creation_user=user)
            else:
                self.fields['cust_order'].queryset = CustOrder.objects.all().exclude(Q(_creation_user_id = 5) | Q(_creation_user_id = 6) | Q(_creation_user_id = 7))
 

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
        fields = ["supp_order","memo", "finished_on"]
        labels = {
            'supp_order': _('Bestellung'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am')
            
        }
        widgets = {
            #'order_no': IntegerField()
        }

    if (True):
        # 3. Digitalisierungsstufe
        def __init__(self, suppliers, *args, **kwargs):
            super(Supp_complaint_form, self).__init__(*args, **kwargs)
            self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier__in=suppliers)
    else:
        # 2. Digitalisierungsstufe
        def __init__(self, user, *args, **kwargs):
            super(Supp_complaint_form, self).__init__(*args, **kwargs)
            if user != 0:
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(_creation_user=user)
            else:
                self.fields['supp_order'].queryset = SuppOrder.objects.all().exclude(Q(_creation_user_id = 20) | Q(_creation_user_id = 21) | Q(_creation_user_id = 22))
                


class Cust_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)

    class Meta:
        model = CustComplaintDet
        fields = ["pos","cust_order_det","memo"]
        labels = {
            'pos': _('Position'),
            'cust_oder_det': _('Position'),
            'memo': _('Kommentar')
        }
    
    def __init__(self, cust_order_id, *args, **kwargs):
        super(Cust_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['cust_order_det'].queryset = CustOrderDet.objects.filter(cust_order_id= cust_order_id)

class Supp_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    finished_on = IntegerField(required=False)

    class Meta:
        model = SuppComplaintDet
        fields = ["pos","supp_order_det","quantity","memo", "finished_on"]
        labels = {
            'pos': _('Position'),
            'supp_oder_det': _('Teil'),
            'quantity': _('Menge'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am'),            
        }
        widgets = {
            #'order_no': IntegerField()
        }

    def __init__(self, supp_order_id, *args, **kwargs):
        super(Supp_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['supp_order_det'].queryset = SuppOrderDet.objects.filter(supp_order_id= supp_order_id)
