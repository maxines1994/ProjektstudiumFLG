from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Supp_complaint_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    finished_on = IntegerField(required=False)

    class Meta:
        model = SuppComplaint
        fields = ["supp_order", "memo", "finished_on", "box_no"]
        labels = {
            'supp_order': _('Bestellung'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am')
            
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
        def __init__(self, suppliers, *args, **kwargs):
            super(Supp_complaint_form, self).__init__(*args, **kwargs)
            if len(suppliers) == 1:
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier__in=suppliers, external_system=True).order_by('_creation_date')
            else:
                self.fields['supp_order'].queryset = SuppOrder.objects.filter(supplier__in=suppliers, external_system=False).order_by('_creation_date')


class Cust_complaint_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)

    class Meta:
        model = CustComplaintDet
        fields = ["cust_order_det", "memo", "box_no"]
        labels = {
           # 'pos': _('Position'),
            'cust_oder_det': _('Position'),
            'memo': _('Kommentar')
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
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
        fields = [ "supp_order_det", "quantity", "memo", "finished_on","redelivery"]
        labels = {
            #'pos': _('Position'),
            'supp_oder_det': _('Teil'),
            'quantity': _('Menge'),
            'memo': _('Kommentar'),
            'finished_on': _('Abgeschlossen am'),
            'redelivery': _('Neulieferung erforderlich'),            
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }

    def __init__(self, supp_order_id, *args, **kwargs):
        super(Supp_complaint_det_form, self).__init__(*args, **kwargs)
        self.fields['supp_order_det'].queryset = SuppOrderDet.objects.filter(supp_order_id= supp_order_id)
