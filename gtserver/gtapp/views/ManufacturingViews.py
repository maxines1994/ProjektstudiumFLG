from gtapp.utils import get_context, get_context_back
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from gtapp.models import CustOrderDet, Stock, ArtiPart, SuppOrderDet, Delivery, CustComplaintDet, SuppComplaintDet, SuppComplaint, SuppOrder
from django.views.generic import CreateView
from gtapp.constants import *
from django.forms import modelformset_factory, ModelChoiceField, NumberInput, Select
from gtapp.forms import formset_goods_cust, formset_goods_cust_c, formset_goods_supp, formset_goods_supp_c
from django.urls import resolve
from django.contrib.auth.decorators import login_required

@login_required
def manufacturing_list_view(request):
    c = {}
    c["manufacturing"] = CustOrderDet.objects.filter(cust_order__external_system=False, status__gte=CustOrderDet.Status.BESTANDSPRUEFUNG_AUSSTEHEND, status__lte=CustOrderDet.Status.LIEFERUNG_AN_K_AUSSTEHEND)
    c["manufacturing_complaints"] = CustOrderDet.objects.filter(id__in=CustComplaintDet.objects.filter(status__gte=CustComplaintDet.Status.ERFASST).values('cust_order_det_id'),cust_order__external_system=False)
    c["complaints"] = CustComplaintDet.objects.filter(cust_order_det__in=c["manufacturing_complaints"])
    c["mylist"] = zip(c["manufacturing_complaints"], c["complaints"])

    if 'complaint' not in resolve(request.path_info).url_name:
        template = "manufacturing.html"
        c["STATUS"] = CustOrderDet.Status.__members__
    else:
        template = "ManufacturingComplaints.html"
        c["STATUS"] = CustComplaintDet.Status.__members__
    return render(request, template, c)

@login_required
def manufacturing_release_view(request, **kwargs):
    c = {}
    return HttpResponseRedirect(reverse("cust_order"))

@login_required
def manufacturing_testing_view(request, **kwargs):
    from .StatusViews import set_status
    c = {}

    demand = CustOrderDet.objects.get(pk=kwargs["id"]).part_demand()
    if Stock.reserve_test(demand):
        print("ERFOLGREICH")
        set_status('CustOrderDet', kwargs["id"], CustOrderDet.Status.BESTANDSPRUEFUNG_ABGESCHLOSSEN) # war vorher '2' von Maxi
    else:
        print("FEHLGESCHLAGEN")
    # SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))

@login_required
def manufacturing_supporder_view(request, **kwargs):
    c = {}
    
    return HttpResponseRedirect(reverse(""))

@login_required
def manufacturing_stock_view(request, **kwargs):
    c = {}
    if request.user.groups.filter(name=JOGA).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=False)

    if request.user.groups.filter(name=L100).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=1)
    
    if request.user.groups.filter(name=L200).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=2)
    
    if request.user.groups.filter(name=L300).exists():
        c["stock"] = Stock.objects.filter(is_supplier_stock=True, part__supplier_id=3)

    return render(request, "stock.html", c)

@login_required
def goods_receipt_view(request, **kwargs):
    template = 'goods_receipt.html'
    MyFormSet = None

    # Erstellung der unterschiedlichen Formsets und definierung der Felder + Widgets
    if kwargs['typeofdet'] == 1: # CustOrderDet
        myextra = CustOrderDet.objects.filter(cust_order_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            Delivery,
            fields=['cust_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'cust_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 2: # CustComplaintDet
        myextra = CustComplaintDet.objects.filter(cust_complaint_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            Delivery,
            fields=['cust_complaint_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'cust_complaint_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 3: # SuppOrderDet
        myextra = SuppOrderDet.objects.filter(supp_order_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            Delivery,
            fields=['supp_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'supp_det': Select(attrs={'disabled':True})
            }
            )
    if kwargs['typeofdet'] == 4: # SuppComplaintDet
        myextra = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs['idofdet']).count()
        MyFormSet = modelformset_factory(
            Delivery,
            fields=['supp_complaint_det', 'quantity', 'delivered', 'trash'],
            extra=myextra,
            widgets={
                'quantity': NumberInput(attrs={'readonly':True}),
                'supp_complaint_det': Select(attrs={'disabled':True})
            }
            )

    # Verarbeitung des Post Requests zur Speicherung der abgeschickten Form
    if request.method == 'POST':
        fs = MyFormSet(request.POST, queryset=Delivery.objects.none(), prefix="form1")
        # Form Valid?
        if fs.is_valid():
            fsets = fs.save(commit=False)
            doc = list()

            # Durchgehen aller Forms innerhalb des Formsets
            for fset in fsets:
                fset._creation_user = request.user
                fset.save()
                doc.append(fset.id)
            
            c = None

            # ERSTELLUNG DER REKLAMATIONEN
            if kwargs['typeofdet'] == 1:
                # TBD
                pass
            if kwargs['typeofdet'] == 2:
                # TBD
                pass

            if kwargs['typeofdet'] == 3:
                bo = False
                for i in doc:
                    if Delivery.objects.filter(pk=i)[0] != 0:
                        bo = True
                if bo:
                    c = SuppComplaint.objects.create(supp_order_id=kwargs['idofdet'])
                    for i in doc:
                        rd = Delivery.objects.get(pk=i)
                        if rd.trash != 0: # POSNR AUTOMATISCH ?!
                            SuppComplaintDet.objects.create(pos=i, supp_complaint_id=c.pk, supp_order_det_id=kwargs["idofdet"], quantity=rd.trash)
                return HttpResponseRedirect(reverse("supp_order_alter",args=[kwargs['idofdet'],]))
            if kwargs['typeofdet'] == 4:
                return HttpResponseRedirect(reverse("supp_complaint_alter",args=[kwargs['idofdet'],]))
    else:
        initial = []
        qset = None
        if kwargs['typeofdet'] == 1:
            qset = CustOrderDet.objects.filter(cust_order_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"cust_det":i.pk, "quantity":1})
        if kwargs['typeofdet'] == 2:
            qset = CustComplaintDet.objects.filter(cust_complaint_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"cust_complaint_det":i.pk, "quantity":1})
        if kwargs['typeofdet'] == 3:
            qset = SuppOrderDet.objects.filter(supp_order_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"supp_det":i.pk, "quantity":i.quantity})
        if kwargs['typeofdet'] == 4:
            qset = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs['idofdet'])
            for i in qset:
                initial.append({"supp_complaint_det":i.pk, "quantity":i.quantity})
        formset = MyFormSet(initial=initial, queryset=Delivery.objects.none(), prefix='form1')
    return render(request, template, {'formset':formset})

@login_required
def goods_shipping_view(request, **kwargs):
    template = 'Goods_Shipping.html'
    MyFormSet = None
