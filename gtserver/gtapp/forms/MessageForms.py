from gtapp.forms import *
from django.utils.translation import gettext_lazy as _
from gtapp.constants import *
from django.contrib.auth.models import Group, User
from django.db.models import Q

class Msg_write_form(ModelForm):
    use_required_attribute = False
    
    def __init__(self,user,*args,**kwargs):
        super(Msg_write_form, self).__init__(*args, **kwargs)
        if user.groups.filter(name=LIEFERANTEN).exists():
            self.fields["receiver"] = ModelChoiceField(queryset=Group.objects.filter(Q(name=PRODUKTIONSDIENSTLEISTUNG)|Q(name=LEITUNGSTEAM)), label="Empfänger")
        elif user.groups.filter(name=KUNDEN).exists():
            self.fields["receiver"] = ModelChoiceField(queryset=Group.objects.filter(Q(name=PRODUKTIONSDIENSTLEISTUNG)|Q(name=LEITUNGSTEAM)), label="Empfänger")
        elif user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists():
            self.fields["receiver"] = ModelChoiceField(queryset=Group.objects.all().exclude(name=KUNDEN), label="Empfänger")
        elif user.groups.filter(name=KUNDENDIENST).exists():
            self.fields["receiver"] = ModelChoiceField(queryset=Group.objects.all().exclude(name=LIEFERANTEN), label="Empfänger")
        else:
            self.fields["receiver"] = ModelChoiceField(queryset=Group.objects.all().exclude(Q(name=LIEFERANTEN)|Q(name=KUNDEN)), label="Empfänger")

    class Meta:
        model = Message
        fields = ["receiver", "subject", "text"]
        labels = {
            'receiver': 'Empfänger',
            'subject': 'Betreff',
            'text': 'Nachricht',
        }
