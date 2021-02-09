from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class formset_goods_cust(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['cust_det'].disabled = True
            self.fields['quantity'].disabled = True

    class Meta:
        fields = ['cust_det', 'quantity', 'delivered', 'trash']


class formset_goods_cust_c(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['cust_complaint_det'].disabled = True
            self.fields['quantity'].disabled = True

    class Meta:
        fields = ['cust_complaint_det', 'quantity', 'delivered', 'trash']


class formset_goods_supp(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['supp_det'].widget.attrs['readonly'] = True
            self.fields['quantity'].widget.attrs['readonly'] = True

    class Meta:
        fields = ['supp_det', 'quantity', 'delivered', 'trash']


class formset_goods_supp_c(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['supp_complaint_det'].widget.attrs['readonly'] = True
            self.fields['quantity'].widget.attrs['readonly'] = True

    class Meta:
        fields = ['supp_complaint_det', 'quantity', 'delivered', 'trash']
