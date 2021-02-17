from django.db import models
from gtapp.models import GtModel
from gtapp.models import CustOrder, SuppOrder, CustComplaint, SuppComplaint, SuppOrderDet, CustOrderDet, CustComplaintDet, SuppComplaintDet, Stock, BookingCode, ArtiPart
from gtapp.constants import *


class Delivery(GtModel):
    cust_order = models.ForeignKey(CustOrder, null=True, on_delete=models.CASCADE, verbose_name="Auftrag")
    cust_order_det = models.ForeignKey(CustOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_order = models.ForeignKey(SuppOrder, null=True, on_delete=models.CASCADE, verbose_name="Bestellung")
    supp_order_det = models.ForeignKey(SuppOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    cust_complaint = models.ForeignKey(CustComplaint, null=True, on_delete=models.CASCADE, verbose_name="Auftragsreklamation")
    cust_complaint_det = models.ForeignKey(CustComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_complaint = models.ForeignKey(SuppComplaint, null=True, on_delete=models.CASCADE, verbose_name="Bestellreklamation")
    supp_complaint_det = models.ForeignKey(SuppComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    artipart = models.ForeignKey(ArtiPart, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    quantity = models.IntegerField(verbose_name="Menge")
    delivered = models.IntegerField(verbose_name="Geliefert")
    trash = models.IntegerField(blank=True, null=True, verbose_name="Davon fehlerhaft", default=0)

    def save(self, *args, **kwargs):
        """
        Dient zum Schreiben von Lagerbewegungen von Bestellungen und Bestellreklamationen
        """
        complaint = False
        supp = False
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
        
        # Je nach Art des Wareneingangs wird die ID des Kopfdatensatzes mitgespeichert, 
        # der entsprechende Lagerbestand geaendert und eine Lagerbewegung geschrieben.
        if supp:
            #SuppComplaint
            if complaint:
                self.supp_complaint = SuppComplaint.objects.get(id=SuppComplaintDet.objects.get(id=self.supp_complaint_det_id).supp_complaint_id)
                Stock.objects.get(is_supplier_stock=external_system, part=self.supp_complaint_det.supp_order_det.part).change(my_delivery_amount)
            #SuppOrder
            else:
                self.supp_order = SuppOrder.objects.get(id=SuppOrderDet.objects.get(id=self.supp_order_det_id).supp_order_id)
                Stock.objects.get(is_supplier_stock=external_system, part=self.supp_order_det.part).change(my_delivery_amount)
        else: 
            #CustComplaint
            if complaint:
                self.cust_complaint = CustComplaint.objects.get(id=CustComplaintDet.objects.get(id=self.cust_complaint_det_id).cust_complaint_id)
            #CustOrder
            else:
                self.cust_order = CustOrder.objects.get(id=CustOrderDet.objects.get(id=self.cust_order_det_id).cust_order_id)
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

        


        
