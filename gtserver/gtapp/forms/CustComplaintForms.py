from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Cust_complaint_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = CustComplaint
        fields = ["cust_order", "memo"]
        labels = {
            'cust_order': _('Auftrag'),
            'memo': _('Kommentar'),
        }
        widgets = {
            #'order_no': IntegerField()
        }

    #"False" muss durch "False" ausgetauscht werden für den produktiven Betrieb
    if (False):
        # 3. Digitalisierungsstufe
        def __init__(self, customers, *args, **kwargs):
            super(Cust_complaint_form, self).__init__(*args, **kwargs)
            self.fields['cust_order'].queryset = CustOrder.objects.filter(customer__in=customers)
    else:
        # 2. Digitalisierungsstufe
        def __init__(self, customers, *args,  **kwargs):
            super(Cust_complaint_form, self).__init__(*args, **kwargs)
            if len(customers) == 1:
                self.fields['cust_order'].queryset = CustOrder.objects.filter(customer__in=customers, external_system=True)
            else:
                self.fields['cust_order'].queryset = CustOrder.objects.all().filter(customer__in=customers, external_system=False)
 