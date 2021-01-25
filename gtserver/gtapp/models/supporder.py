from django.db import models
from gtapp.models.custorderdet import CustOrderDet
from . import Order, Supplier, CustOrder

class SuppOrder(Order):
    """
    Diese Model enthaelt die Kopfdaten der Lieferantenbestellungen.
    """   

    cust_order_det = models.ForeignKey(CustOrderDet, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    
    
    def __str__(self):
        return ("Bestellung " + self.order_no)

    def auto_needs(self):
        cod = CustOrderDet.objects.get(pk=self.pk)
        needs = list()
        atpt = ArtiPart.objects.filter(article_id=cod.article.id, part__supplier_id=3)
        for p in atpt:
            needs.append((p.part, p.quantity))
        return needs
    
    