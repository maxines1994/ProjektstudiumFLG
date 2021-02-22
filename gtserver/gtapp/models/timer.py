from django.db import models
from django.db import connection
import datetime

class Timers(models.Model):
    nowactive = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #day = models.SmallIntegerField()
    #speed..
    
    @classmethod
    def get_current_day(cls):
        sum = 0
        nowtime = datetime.datetime.now()
        # Erst reinspringen, wenn diese Tabelle bereits existiert, sonst knallts bei den makemigrations,
        # weil Tasks ein get_current_day aufruft
        if Timers._meta.db_table in connection.introspection.table_names():
            myList = list(Timers.objects.all().order_by('timestamp'))
            for i in myList:
                if i.nowactive:
                    sum -= i.timestamp.timestamp()
                else:
                    sum += i.timestamp.timestamp()
            

            if len(myList) != 0:
                if myList[-1].nowactive:
                    sum += nowtime.timestamp()

        return int(sum/5+1)
