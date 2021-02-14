from django.db import models
from gtapp.models import GtModel
from gtapp.models import SuppOrderDet, CustOrderDet, CustComplaintDet, SuppComplaintDet, Stock, BookingCode, ArtiPart
from gtapp.constants import *


class Delivery(GtModel):
    cust_order_det = models.ForeignKey(CustOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_order_det = models.ForeignKey(SuppOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    cust_complaint_det = models.ForeignKey(CustComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_complaint_det = models.ForeignKey(SuppComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    artipart = models.ForeignKey(ArtiPart, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    quantity = models.IntegerField(verbose_name="Menge")
    delivered = models.IntegerField(verbose_name="Geliefert")
    trash = models.IntegerField(null=True, blank=True, verbose_name="Davon fehlerhaft", default=0)

    def save(self, *args, **kwargs):
        """
        Dient zum Schreiben von Lagerbewegungen von Bestellungen und Bestellreklamationen
        """
        complaint = False
        supp_order = False
        external_system = True

        if self._creation_user.groups.filter(name=JOGA).exists():
            external_system = False

        # Ist die Liefermenge positiv, handelt es sich um einen Wareneingang. 
        # Dieser muss um die Menge der fehlerhaften Teile bereinigt werden, # bevor ins Lager gebucht wird.  
        if self.delivered > 0:
            my_delivery_amount = self.delivered - self.trash
        # Bei Warenausgaengen kann die Liefermenge einfach uebernommen werden.
        else:
            my_delivery_amount = self.delivered

        # Nichts speichern, wenn nichts geliefert wurde.
        if my_delivery_amount == 0:
            return 0

        # Herausfinden welche Art von Wareneingang erfolgt. Es ist immer nur einer der Fremdschluessel
        # gefuellt und dementsprechend werden die boolschen Felder cust_order, supp_order und/oder complaint gesetzt.
        for field in Delivery._meta.fields:
            if field.get_internal_type() == 'ForeignKey' and not field.name.startswith("_"): #Keine Metadaten abfragen
                if getattr(self, field.name) is not None:
                    if 'supp' in field.name :
                        supp = True

                    if 'complaint' in field.name :
                        complaint = True
        
        if supp:
            if complaint:
                Stock.objects.get(is_supplier_stock=external_system, part=self.supp_complaint_det.supp_order_det.part).change(my_delivery_amount)
            else:
                Stock.objects.get(is_supplier_stock=external_system, part=self.supp_order_det.part).change(my_delivery_amount)
        else: 
            Stock.objects.get(is_supplier_stock=external_system, part=self.artipart.part).change(my_delivery_amount)
        
        return super(Delivery, self).save(*args, **kwargs)
        """
        #Brauchen wir ab hier noch irgendwas?
        # Abfragen der Art des Wareneingangs
        if cust_order:
            if complaint:
                # TBD
                pass


        


        # STATUS SETZEN

        # REKLAMATION ERSTELLEN
        
        """

        
