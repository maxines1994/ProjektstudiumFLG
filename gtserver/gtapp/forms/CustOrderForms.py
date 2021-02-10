from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Cust_order_form_jg(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    #refno = CharField(required=False)

    class Meta:
        model = CustOrder
        fields = ["ref_no", "customer", "issued_on",
                  "delivery_date", "memo"]

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
        fields = ["issued_on", "delivery_date", "memo", "box_no"]



class Cust_order_det_form(ModelForm):
    use_required_attribute = False
    memo = CharField(required=False)
    unit_price = IntegerField(required=False)

    class Meta:
        model = CustOrderDet
        fields = ["pos", "article", "unit_price", "memo", "box_no"]
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