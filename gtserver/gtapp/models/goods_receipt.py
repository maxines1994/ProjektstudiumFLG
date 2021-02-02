from django.db import models
from gtapp.models import GtModel
from gtapp.models import SuppOrderDet, CustOrderDet, CustComplaintDet, SuppComplaintDet, Stock, BookingCode

class goods_receipt(GtModel):
    cust_det = models.ForeignKey(CustOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_det = models.ForeignKey(SuppOrderDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    cust_complaint_det = models.ForeignKey(CustComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    supp_complaint_det = models.ForeignKey(SuppComplaintDet, null=True, on_delete=models.CASCADE, verbose_name="Ware")
    quantity = models.IntegerField(verbose_name="Menge")
    delivered = models.IntegerField(verbose_name="Geliefert")
    trash = models.IntegerField(null=True, blank=True, verbose_name="Davon fehlerhaft", default=0)

    def save(self, *args, **kwargs):
        external_system = True
        if self._creation_user.groups.filter(name="Joga").exists():
            external_system = False
        
        bc = BookingCode.objects.filter(code="REC")[0]

        # Abfragen der Art des Wareneingangs
        if self.cust_det is not None:
            # TBD
            pass

        elif self.supp_det is not None:
            Stock.objects.filter(is_supplier_stock=external_system, part=self.supp_det.part)[0].change(self.delivered)

        elif self.cust_complaint_det is not None:
            # TBD
            pass

        elif self.supp_complaint_det is not None:
            Stock.objects.filter(is_supplier_stock=external_system, part=self.supp_det.part)[0].change(self.delivered)
        
        # STATUS SETZEN

        # REKLAMATION ERSTELLEN
        

        return super(goods_receipt, self).save(*args, **kwargs)
        
