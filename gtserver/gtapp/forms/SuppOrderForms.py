from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Supp_order_form_jg(ModelForm):
    use_required_attribute = False

    class Meta:
        model = SuppOrder
        fields = ["ref_no", "issued_on", "supplier", "delivery_date", "memo", "box_no"]
        labels = {
            "order_no": _("Referenznummer"),
            "issued_on": _("Bestelldatum"),
            "supplier": _("Lieferant"),
            "delivery_date": _("Lieferdatum"),
            'memo': _('Kommentar'),
        }


class Supp_order_form_lf(ModelForm):
    use_required_attribute = False

    issued_on =  IntegerField(
        label=_("Bestelltag"),
    )
    delivery_date =  IntegerField(
        label=_('Liefertag'),
    )

    memo = CharField(
        label=_('Kommentar'),
        required = False,
        widget=Textarea,
    )

    class Meta:
        model = SuppOrder
        fields = ["ref_no", "issued_on", "delivery_date", "memo", "box_no"]
        labels = {
            'memo': _('Kommentar'),
        }

class Supp_order_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)

    class Meta:
        model = SuppOrderDet
        fields = ["part", "quantity", "memo"]
        labels = {
            #'pos': _('Positionsnummer'),
            'part': _('Artikel'),
            'quantity': _('Menge'),
            'memo': _('Kommentar'),
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }

    def __init__(self, parts, *args, **kwargs):
        super(Supp_order_det_form, self).__init__(*args, **kwargs)
        self.fields['part'].queryset = parts
