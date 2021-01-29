from django.db import models
from gtapp.models import Timers

"""
Hier alle Settings einsetzen, die live abgefragt bzw. live geändert werden sollen.

Usage: "LiveSettings.load()"
"""

class LiveSettings(models.Model):
    debugflag = models.BooleanField(default=True)
    timeactive = models.BooleanField(default=False)
    phase_3 = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        self.pk = 1

        if LiveSettings.objects.filter(pk=1).exists():
            #Check for TimeActiveChange
            if self.timeactive != LiveSettings.load().timeactive:
                Timers.objects.create(nowactive=self.timeactive)

        super(LiveSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
