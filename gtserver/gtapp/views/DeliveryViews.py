from gtapp.utils import get_context
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, DetailView
from gtapp.models import Task, TaskType, CustOrder, SuppOrder, CustOrderDet, SuppOrderDet, GtModel, Delivery, Part, Timers
from django.contrib.auth.models import Group, User
from gtapp.constants import *
from gtapp.views.StatusViews import set_status 
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
    # Bin ich Lieferant?
    is_supplier = request.user.groups.filter(name=LIEFERANTEN).exists()
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
    my_foreign_key_on_goods_shipping = get_fieldname(model=Delivery, foreign_key_model=my_model_det) if kwargs['model'] != CustOrderDet.__name__ else 'artipart'

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
    
    if request.method == 'POST':
        fs = MyFormSet(request.POST, queryset=Delivery.objects.none(), prefix="form1")
        # Form Valid?
        if fs.is_valid():
            fsets = fs.save(commit=False)
            my_supp_order_det_id_list = []
            my_trash_list = []
            doc = list()

            # Durchgehen aller Forms innerhalb des Formsets
            for fset in fsets:
                fset.delivered *= delivery_multiplier
                fset._creation_user = request.user
                # CustOrderDet-ID explizit wegspeichern, weil das formset bei CustOrderDets mit der arti_part_id
                # gefuellt wird und nicht mit der cust_order_det_id
                if my_model == CustOrderDet:
                    fset.cust_order_det_id = kwargs['id']
                # Reservierungen bei den Bestaenden um entnommene Menge reduzieren
                if is_shipping:
                    if my_model == CustOrderDet:
                        my_part = Part.objects.get(id=ArtiPart.objects.get(id=fset.artipart_id).part_id)
                    elif my_model == SuppComplaint:
                        my_part = Part.objects.get(id=SuppOrderDet.objects.get(id=fset.supp_complaint_det.supp_order_det_id).part_id)
                    elif my_model == SuppOrder:
                        my_part = Part.objects.get(id=SuppOrderDet.objects.get(id=fset.supp_order_det_id).part_id)
                    else:
                        my_part = Part.objects.get(id=my_model_det.objects.get(id=kwargs['id']).part_id)
                       
                    my_stock = Stock.objects.get(is_supplier_stock=is_supplier,part=my_part)
                    # Reservierte Menge um zu liefernde Menge verringern
                    my_stock.reserve(-fset.quantity)
                
                else:
                    if my_model == SuppOrder:
                        my_part = Part.objects.get(id=SuppOrderDet.objects.get(id=fset.supp_order_det_id).part_id)
                        # Zusaetzlich Teile und Mengen der Falschteile in Liste schreiben um spaeter
                        # automatische Reklamationen zu erzeugen
                        if fset.trash > 0:
                            my_supp_order_det_id_list.append(fset.supp_order_det_id)
                            my_trash_list.append(fset.trash)

                        # Bei Wareneingaengen von Bestellungen den Status der Bestellung auf teilgeliefert setzen,
                        # wenn er kleiner ist als teilgeliefert.
                        my_supporder_qry = SuppOrder.objects.filter(id=kwargs['id'])
                        if my_supporder_qry.first().status < SuppOrder.Status.TEILGELIEFERT:
                            my_supporder_qry.update(status=SuppOrder.Status.TEILGELIEFERT)

                fset.save()
            
            # Automatische Bestellreklamation erzeugen.
            if len(my_supp_order_det_id_list) > 0:
                new_supp_complaint_id = SuppComplaintDet.auto_complaint(supp_order_det_id_list=my_supp_order_det_id_list, quantity_list=my_trash_list)

            # Tasks und Status setzen
            previous = request.POST.get('previous') 
            next_url = previous if previous is not None else "home"
            mykwargs = {}
            mykwargs['id'] = kwargs['id']

            if my_model == CustOrderDet:
                if request.user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists():
                    next_url = "set_status_call" # Nach Warenentnahme fuer Produktion wieder zurueck zu Fertigungsauftraegen
                    mykwargs['model'] = kwargs['model']
                    mykwargs['status'] = CustOrderDet.Status.AUFTRAG_FREIGEGEBEN
            if my_model == SuppOrder:
                if request.user.groups.filter(name=LIEFERANTEN).exists():
                    next_url = "set_status_call"
                    mykwargs['model'] = kwargs['model']
                    mykwargs['status'] = SuppOrder.Status.GELIEFERT
                if request.user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists():
                    # Task erzeugen zur Freigabe der Bestellreklamation und Weiterleitung zu Aufgabenpool
                    if len(my_supp_order_det_id_list) > 0:
                        next_url = "set_status_task"
                        mykwargs['id'] = new_supp_complaint_id
                        mykwargs['task_type'] = 38

            if my_model == SuppComplaint:
                if request.user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists():
                    my_supp_complaint_dets = SuppComplaintDet.objects.filter(supp_complaint_id=kwargs['id'])

                    for item in my_supp_complaint_dets:
                        set_status(SuppComplaintDet.__name__, item.id, SuppComplaintDet.Status.VERSAND_AN_LIEFERANT)
                    return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs=mykwargs))

            if len(mykwargs) > 1:
                # Redirect mit Parameter
                return HttpResponseRedirect(reverse(next_url, kwargs=mykwargs))

            else:
                # Wenn auf die vorherige Seite geleitet werden soll, brauchen wir kein reverse
                if next_url == previous:
                    return HttpResponseRedirect(next_url)
                # Ansonsten redirect ohne Parameter
                
                return HttpResponseRedirect(reverse(next_url))
    else:
        initial = []
        for_iterator = 0
        if my_model == CustOrderDet:
            qset = ArtiPart.objects.filter(**my_model_id)
            for i in qset:
                quantity = i.quantity 
                initial.append({my_foreign_key_on_goods_shipping:i.pk, "quantity":quantity})
        else:
            qset = my_model_det.objects.filter(**my_model_id)
            for i in qset:
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
