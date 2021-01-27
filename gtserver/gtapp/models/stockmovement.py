from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from gtapp.constants import *
from . import GtModel, Stock, BookingCode, Translation

class StockMovement(GtModel):
    """
    Dieses Model speichert den Verlauf eines Bestandes in Form von Lagerbewegungen.
    """

    date = models.SmallIntegerField()
    previous_stock = models.SmallIntegerField()
    booking_quantity = models.SmallIntegerField()
    new_stock = models.SmallIntegerField()
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    booking_code = models.ForeignKey(BookingCode, on_delete=models.CASCADE)

    def append(previous_stock: int, booking_quantity: int, stock: Stock, booking_code=BOOKING_UNKNOWN):
        """
        Fuegt eine neue Lagerbewegung hinzu. Der booking_code muss nur uebergeben werden, wenn es sich um eine besondere Buchung, wie eine Inventur
        oder eine Systemkorrektur handelt. Diese Methode ermittelt anhand der booking_quantity, ob es sich um eine Entnahme oder einen Wareneingang handelt.
        Ist die booking_quantity >= 0 ist es ein Wareneingang, sonst eine Entnahme.
        """

        try:
            #Wenn kein Buchungscode explizit uebergeben wird, entscheide anhand der gebuchten Menge, ob es eine Entnahme oder ein Wareneingang ist
            if booking_code == BOOKING_UNKNOWN:
                if booking_quantity >= 0:
                    booking_code = BOOKING_GOODS_RECEIPT
                else:
                    booking_code = BOOKING_GOODS_WITHDRAWAL

            myBooking_code = BookingCode.objects.get(code=booking_code)
           
            #date muss hier noch durch eine Funktion ersetzt werden, die das aktuelle Spieldatum zurueckgibt, getDate() oder so.
            StockMovement.objects.create(date=1, previous_stock=previous_stock, booking_quantity=booking_quantity, new_stock=previous_stock + booking_quantity, stock=stock, booking_code=myBooking_code)
        
        except ObjectDoesNotExist:
            raise Exception("Booking-Code " + booking_code + " does not exist")

        