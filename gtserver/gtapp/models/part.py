from django.db import models
from . import Status, Supplier

class Part(models.Model):
   """
   This model contains information about the parts that make up a lifting platform.
   They can be purchased from suppliers.
   """

   status = models.ForeignKey(Status,null=True, on_delete=models.SET_NULL)
   part_no = models.CharField(max_length=8)
   description = models.CharField(max_length=30)
   unit_price = models.SmallIntegerField(null=True)
   picture = models.BinaryField(null=True)
   supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)
   pack_quantity = models.SmallIntegerField()
   install_quantity = models.SmallIntegerField()
   initial_stock = models.SmallIntegerField()
