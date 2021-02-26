from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Cust_order_form_jg(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")
    #refno = CharField(required=False)

    class Meta:
        model = CustOrder
        fields = ["ref_no", "customer", "issued_on",
                  "delivery_date", "memo"]
        labels = {
            'ref_no': _('Referenznummer'),
            'customer': _('Kunde'),
            'issued_on': _('Bestelltag'),
            'delivery_date': _('Liefertag'),
            'memo': _('Kommentar'),

        }

class Cust_order_form_kd(ModelForm):
    use_required_attribute = False

    issued_on = IntegerField(
        label=_("Bestelltag"),
    )
    delivery_date = IntegerField(
        label=_('Liefertag'),
    )
    
    memo = CharField(
        label=_('Kommentar'),
        required = False,
        widget=Textarea,
    )

    class Meta:
        model = CustOrder
        fields = ["issued_on", "delivery_date", "memo"]



class Cust_order_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = CustOrderDet
        fields = ["pos", "article", "memo", "box_no"]
        labels = {
            'pos': _('Positionsnummer'),
            'article': _('Artikel'),
            'memo': _('Kommentar'),
            'box_no': _('Boxnummer'),
        }
        widgets = {
            'pos': TextInput(attrs={'disabled': True}),
        }


class Cust_order_det_form_create(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False, label="Kommentar")

    class Meta:
        model = CustOrderDet
        fields = ["article", "memo"]
        labels = {
            'article': _('Artikel'),
            'memo': _('Kommentar'),
        }
