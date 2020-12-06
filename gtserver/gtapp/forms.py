from django import forms
from django.forms import inlineformset_factory
from gtapp.models import Article, CustOrder, CustOrderDet, Customer

class Cust_order_form(forms.Form):
    Kunde = forms.ModelChoiceField(Customer.objects.all())
    Liefertag = forms.IntegerField()
    Status = forms.CharField(max_length=20)
    Kommentar = forms.CharField(max_length=200)
    jsonitems = forms.CharField(widget=forms.HiddenInput(), label=False)
    
    
