from django.db import models
from gtapp.constants import *
from . import GtModel, Supplier, BookingCode

class Part(GtModel):
  """
  Dieses Model enthaelt Stammdaten der Teile, aus denen die Hubbuehnen bestehen.
  """

  part_no = models.CharField(max_length=8)
  description = models.CharField(max_length=30)
  unit_price = models.SmallIntegerField(null=True)
  image = models.CharField(max_length=30)
  pack_quantity = models.SmallIntegerField()
  install_quantity = models.SmallIntegerField()
  initial_stock = models.SmallIntegerField()
  total_stock = models.SmallIntegerField()
  supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    return str(self.description + " (SM: "+ str(self.pack_quantity) +")" )

  def change_stock(self, of_supplier: bool, booking_quantity: int, booking_code=BOOKING_UNKNOWN):
    """
    Aendert den Bestand dieses Teils und schreibt eine entsprechende Lagerbewegung. Der booking_code muss nur uebergeben werden, wenn es sich um eine 
    besondere Buchung, wie eine Inventur oder eine Systemkorrektur handelt. Diese Methode ermittelt anhand der booking_quantity, ob es sich um eine 
    Entnahme oder einen Wareneingang handelt. Ist die booking_quantity >= 0 ist es ein Wareneingang, sonst eine Entnahme.

    Beispiel:
        myPart.change_stock(BOOKING_INVENTORY_CORRECTION, 2)
    Erhoeht den Bestand um 2 und schreibt eine entsprechende Lagerbewegung mit dem Buchungscode INV.
    """
    from . import Stock
    myStock = Stock.objects.filter(part=self, supplier_stock=of_supplier).first()
    myStock.change(booking_code, booking_quantity)
