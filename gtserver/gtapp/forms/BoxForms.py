from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Box_form(ModelForm):
    use_required_attribute = False

    class Meta:
        model = CustOrderDet
        fields = ["box_no"]
        labels = {
            'box_no': _('Boxnummer'),
        }
        widgets = {
            'box_no': TextInput(attrs={'autofocus': True}),
        }