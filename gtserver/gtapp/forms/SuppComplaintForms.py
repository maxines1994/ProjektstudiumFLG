from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Supp_complaint_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = SuppComplaint
        fields = ["supp_order", "memo",  "box_no"]
        labels = {
            'supp_order': _('Bestellung'),
            'memo': _('Kommentar'), 
            'box_no': _('Boxnummer'),     
        }
        widgets = {
            #'order_no': IntegerField()
        }

    #"False" muss durch "LiveSettings.objects.all().first().phase_3" ausgetauscht werden für den produktiven Betrieb
    if (False):
        # 3. Digitalisierungsstufe
        def __init__(self, suppliers, *args, **kwargs):
            super(Supp_complaint_form, self).__init__(*args, **kwargs)
            self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier__in=suppliers).order_by('_creation_date')
    else:
        # 2. Digitalisierungsstufe
        def __init__(self, user_groups, *args, **kwargs):
            super(Supp_complaint_form, self).__init__(*args, **kwargs)

            if user_groups.filter(name=L100).exists():
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier=1, external_system=True).order_by('_creation_date')
            elif user_groups.filter(name=L200).exists():
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier=2, external_system=True).order_by('_creation_date')
            elif user_groups.filter(name=L300).exists():
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier=3, external_system=True).order_by('_creation_date')
            elif user_groups.filter(name=PRODUKTION).exists():
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(id__in=[1,3,5]).order_by('_creation_date')
            else:
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier__in=[1,2,3], external_system=False).order_by('_creation_date')
                


class Cust_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = CustComplaintDet
        fields = ["cust_order_det", "memo", "box_no"]
        labels = {
           # 'pos': _('Position'),
            'cust_order_det': _('Position'),
            'memo': _('Kommentar'),
            'box_no': _('Boxnummer'),
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }
    
    def __init__(self, cust_order_id, *args, **kwargs):
        super(Cust_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['cust_order_det'].queryset = CustOrderDet.objects.filter(cust_order_id= cust_order_id)

class Supp_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = SuppComplaintDet
        fields = [ "supp_order_det", "quantity", "memo","redelivery"]
        labels = {
            #'pos': _('Position'),
            'supp_order_det': _('Teil'),
            'quantity': _('Menge'),
            'memo': _('Kommentar'),
            'redelivery': _('Neulieferung erforderlich'),            
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }

    def __init__(self, supp_order_id, *args, **kwargs):
        super(Supp_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['supp_order_det'].queryset = SuppOrderDet.objects.filter(supp_order_id= supp_order_id)
