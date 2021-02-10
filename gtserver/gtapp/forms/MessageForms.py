from gtapp.forms import *
from django.utils.translation import gettext_lazy as _

class Msg_write_form(ModelForm):
    use_required_attribute = False
    class Meta:
        model = Message
        fields = ["receiver", "subject", "text"]
        labels = {
            'receiver': 'Empfänger',
            'subject': 'Betreff',
            'text': 'Nachricht',
        }