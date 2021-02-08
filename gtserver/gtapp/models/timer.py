from django.db import models
from django.db import connection
import datetime

class Timers(models.Model):
    nowactive = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def get_current_day(cls):
        sum = 0
        nowtime = datetime.datetime.now()
        if Timers in connection.introspection.table_names():
            myList = list(Timers.objects.all().order_by('timestamp'))
            for i in myList:
                if i.nowactive:
                    sum -= i.timestamp.timestamp()
                else:
                    sum += i.timestamp.timestamp()
            

            if len(myList) != 0:
                if myList[-1].nowactive:
                    sum += nowtime.timestamp()

            return int(sum/180+1)
        else:
            return 0
        