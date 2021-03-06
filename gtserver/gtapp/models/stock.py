from django.db import models
from gtapp.constants import *
from . import GtModel, Part, BookingCode, ArtiPart, CustOrder

class Stock(GtModel):
    """
    Dieses Model enthaelt Informationen ueber die Bestaende und reservierten Mengen der einzelnen Teile. 
    Anhand des Kennzeichens "supplier_stock" erkennt man, ob es sich um den Bestand von JOGA (false) oder 
    den Bestand beim zum Teil gehoerenden Lieferanten handelt (true).
    """

    is_supplier_stock = models.BooleanField(default=False)
    stock = models.SmallIntegerField()
    reserved = models.SmallIntegerField(default=0)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)

    def change(self, booking_quantity: int, booking_code=BUCHUNG_UNBEKANNT):
        """
        Aendert den Bestand und schreibt eine entsprechende Lagerbewegung. Der booking_code muss nur uebergeben werden, wenn es sich um eine 
        besondere Buchung, wie eine Inventur oder eine Systemkorrektur handelt. Diese Methode ermittelt anhand der booking_quantity, ob es sich um eine 
        Entnahme oder einen Wareneingang handelt. Ist die booking_quantity >= 0 ist es ein Wareneingang, sonst eine Entnahme.

        Beispiel:
            mystock.change(BUCHUNG_KORREKTURBUCHUNG, 2)
        Erhoeht den Bestand um 2 und schreibt eine entsprechende Lagerbewegung mit dem Buchungscode INV.
        """

        from . import StockMovement
        # booking_quantity nur uebernehmen, wenn der Bestand dadurch mindestens 0 ist.
        # Wuerde er auf unter 0 sinken, wird booking_quantity auf den negativen Wert des aktuellen Bestandes gesetzt.
        # Dadurch faellt der Bestand allenfalls auf 0 und es wird eine korrekte Lagerbewegung geschrieben.
        booking_quantity = booking_quantity if self.stock + booking_quantity >= 0 else -self.stock
        StockMovement.append(previous_stock=self.stock, booking_quantity=booking_quantity, stock=self, booking_code=booking_code)
        self.stock += booking_quantity
        self.save()
    
    def reserve(self, quantity):
        """
        Erhoeht oder verringert die reservierte Menge des Bestandes, je nach Vorzeichen von quantity.
        """
        if self.reserved + quantity >= 0:
            self.reserved += quantity
        else:
            self.reserved = 0
        self.save()
        
    @classmethod
    def reserve_test(cls, needs=list()):
        newNeeds = list()
        for i in needs:
            p, q = i
            nq = 0
            stk = Stock.objects.get(is_supplier_stock=False, part=p)
            reservable = stk.stock-stk.reserved
            if q > reservable:
                nq = q - reservable
            else:
                nq = 0
            newNeeds.append((p, nq))

        for i in newNeeds:
            p, q = i
            if q != 0:
                return False
        return True
