from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Stock_form(ModelForm):
    use_required_attribute = False

    class Meta:
        model = Stock
        fields = ["stock"]
        labels = {
            'stock': _('Bestand'),
        }
