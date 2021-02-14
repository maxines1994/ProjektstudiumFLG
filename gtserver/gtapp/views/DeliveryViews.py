from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Task, TaskType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet, GtModel, Delivery, Part
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.models import Timers
from django import forms
from gtapp.forms import *
import json
from django.urls import resolve
from django.contrib.auth.decorators import login_required

@login_required
def stock_check_view2(request, **kwargs):
    c = {}
    demand = CustOrderDet.objects.get(pk=kwargs["id"]).part_demand()
    print(demand)
    if Stock.reserve(demand=demand):
        print("ERFOLGREICH")
        CustOrderDet.objects.filter(pk=kwargs["id"]).update(status=CustOrderDet.Status.IN_PRODUKTION)
    else:
        print("FEHLGESCHLAGEN")
    # SETSTATUSTO BESTANDSPRÜFUNG GOOD OR BESTANDSPRÜFUNG BAD
    return HttpResponseRedirect(reverse("manufacturing_list"))

@login_required
def delivery_view(request, **kwargs):
    template = 'Delivery.html'
    MyFormSet = None
    #my_model = z.B. CustOrder
    my_model = GtModel.str_to_gtmodel(kwargs['model'])
    # Handelt es sich hierbei um ein Model mit 'det'?
    not_det = "det" not in kwargs['model'].casefold()    
    #Filter initialisieren
    my_model_id = {}
    if not_det:
        # my_model_det entspricht zum Beispiel CustOrderDet (es sei denn my_model ist bereits 'det')
        my_model_det = GtModel.str_to_gtmodel(my_model.__name__ + 'Det')
        # Hier wird ein Filter gebaut, der nach den Positionsdatensätzen des übergebenen Models fahndet
        # Das können CustOrderDets, SuppOrderDets, SuppComplaintDets oder CustComplaintDets sein.
        # Immer wird im richtigen Model nach dem richtigen Fremdschluessel gesucht.
        my_model_id[get_fieldname(model=my_model_det, foreign_key_model=my_model)] = kwargs['id']
    else:
        my_model_det = GtModel.str_to_gtmodel(my_model.__name__)
        my_model_id['article_id'] = 1
        my_model_id['part__supplier_id'] = 3


    # Hier wird der Name des zu belegenden Fremdschluesselfeldes in der Delivery ermittelt
    my_foreign_key_on_goods_shipping = get_fieldname(model=Delivery, foreign_key_model=my_model_det) if not CustOrderDet else 'artipart'
    if my_model == CustOrderDet:
        # Anzahl der Positionen entspricht den Artiparts bei CustOrderDets
        my_pos_count = ArtiPart.objects.filter(article_id__in=my_model.objects.filter(id=kwargs['id']).values('article_id'),part__supplier_id=3).count()
    else:
        # Anzahl der Positionsdatensaetze
        my_pos_count = my_model_det.objects.filter(**my_model_id).count()

    # Warenausgang?
    is_shipping = resolve(request.path_info).url_name == 'goods_shipping'
    
    if is_shipping:
        delivery_multiplier = -1
        delivered_label = 'Entnommen'
    else:
        delivery_multiplier = 1
        delivered_label = 'Geliefert'

    MyFormSet = modelformset_factory(
        Delivery,
        fields=[my_foreign_key_on_goods_shipping, 'quantity', 'delivered', 'trash'],
        extra=my_pos_count,
        labels={
            'delivered': delivered_label,
        },
        widgets={
            'quantity': TextInput(attrs={'disabled':True}),
           my_foreign_key_on_goods_shipping: Select(attrs={'disabled':True}),
           'delivered': TextInput(attrs={'required': 'required'}),
           'trash': NumberInput(attrs={'hidden': is_shipping}),
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
                fset.delivered *= delivery_multiplier
                fset._creation_user = request.user
                fset.save()
                doc.append(fset.id)
            
            c = None
            
            # ERSTELLUNG DER REKLAMATIONEN
            if kwargs['model'] == CustOrderDet:
                # TBD
                pass
            if kwargs['model'] == CustComplaintDet:
                # TBD
                pass

            if kwargs['model'] == SuppOrderDet:
                bo = False
                for i in doc:
                    if Delivery.objects.filter(pk=i)[0] != 0:
                        bo = True
                if bo:
                    c = SuppComplaint.objects.create(supp_order_id=kwargs['id'])
                    for i in doc:
                        rd = Delivery.objects.get(pk=i)
                        if rd.trash != 0: # POSNR AUTOMATISCH ?!
                            SuppComplaintDet.objects.create(pos=i, supp_complaint_id=c.pk, supp_order_det_id=kwargs["idofdet"], quantity=rd.trash)
            if kwargs['model'] == SuppComplaintDet:
                pass
            
            return HttpResponseRedirect(reverse("supp_order"))
    else:
        initial = []
        for_iterator = 0
        if my_model == CustOrderDet:
            qset = ArtiPart.objects.filter(**my_model_id)
            for i in qset:
                quantity = i.quantity 
                
                initial.append({my_foreign_key_on_goods_shipping:i.pk, "quantity":quantity})
        else:
            for i in qset:
                qset = my_model_det.objects.filter(**my_model_id)
                # Setze die Menge zu entnehmender Teile auf die ArtiPart.quantity wenn es sich
                # um eine CustOrderDet handelt, sonst nimm die quantity des det-Datensatzes
                quantity = i.quantity
                part_name = my_foreign_key_on_goods_shipping
                
                initial.append({my_foreign_key_on_goods_shipping:i.pk, "quantity":quantity})
                for_iterator += 1

        formset = MyFormSet(initial=initial, queryset=Delivery.objects.none(), prefix='form1')
        return render(request, template, {'formset':formset})

def get_fieldname(model: GtModel, foreign_key_model: GtModel):
    """
    Diese Funktion sucht die richtige Feldbezeichnung des Fremdschluessels  in der Tabelle "model" 
    anhand des übergebenen Models des Fremdschluessels "foreign_key_model".
    Die Feldbezeichnungen der Fremdschlussel in den Models entsprechen nicht den Namen
    der verknuepften Models. Deshalb wird anhand des Modelnamens das entsprechende Feld gesucht.
    Beispiel:
    In der SuppOrderDet gibt es das Feld "supp_order". Wenn als model "SuppOrderDet" und als
    foreign_key_model "SuppOrder" uebergeben werden, gibt diese Funktion "supp_order" zurück.
    """
    for item in model._meta.fields:
        if item.name.replace("_","") == foreign_key_model.__name__.casefold():
            return str(item.name)
