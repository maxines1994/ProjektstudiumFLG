from . import *


@login_required
def set_status_task (request, **kwargs):
    """
    View zum erzeugen eines neuen Tasks. Dabei wird auch ein neuer Status gesetzt.
    Benoetigte Argumente:

    id          = Objekt, dessen Status gesetzt werden soll und auf den sich Task bezieht
    task_type   = ID des TaskTypes von dem neuer Task erzeugt werden soll.
    """
    # Hol den Status, der fuer diesen TaskType hinterlegt ist.
    my_task_type = TaskType.objects.get(id=kwargs["task_type"])
    #my_status_model = GtModel.str_to_gtmodel(my_task_type.status_model)
    task_type_status = my_task_type.status


    my_task_model = GtModel.str_to_gtmodel(my_task_type.task_model)
    my_task_filter = {}
    # Ist der Flag "task_for_all_details" gesetzt, wird der hinterlegte Task
    # fuer alle Positionsdaten angelegt. Daher lautet der Filter nicht "id = kwargs["id"]"
    # sondern "xxx_order = kwargs["id"]" oder "xxx_complaint = kwargs["id"]"
    if my_task_type.task_for_all_details:
        my_header_model = GtModel.str_to_gtmodel(my_task_type.task_model.replace('Det', ''))
        my_header_field = GtModel.gtmodel_to_foreign_field_name(my_header_model)
        my_task_filter[my_header_field] = kwargs["id"]
    else:
        my_task_filter["id"] = kwargs["id"]
    
    my_status_filter = {}
    # Ist der Flag "status_for_all_details" gesetzt, wird der hinterlegte Status
    # fuer alle Positionsdaten angelegt. Daher lautet der Filter nicht "id = kwargs["id"]"
    # sondern "xxx_order = kwargs["id"]" oder "xxx_complaint = kwargs["id"]"
    if my_task_type.status_for_all_details:
        my_header_model = GtModel.str_to_gtmodel(my_task_type.task_model.replace('Det', ''))
        my_header_field = GtModel.gtmodel_to_foreign_field_name(my_header_model)
        my_status_filter[my_header_field] = kwargs["id"]
    else:
        my_status_filter["id"] = kwargs["id"]

    # Queries aller gefundenen Objekte fuer Tasks und Status
    my_task_obj_qry = my_task_model.objects.filter(**my_task_filter)
    my_status_obj_qry = my_task_model.objects.filter(**my_status_filter)

    # Durchlaeuft das Query der gefundenen Objekte und erzeugt fuer jedes Objekt einen Task.
    for obj in my_task_obj_qry:
        set_status(my_task_type.status_model, obj.id, task_type_status)
        Task.set_task(obj=obj, task_type_id=kwargs["task_type"])
    
    # Durchlaeuft das Query der gefundenen Objekte und setzt fuer jedes Objekt den neuen Status.
    for obj in my_status_obj_qry:
        # An set_status muss das Model wieder als String uebergeben werden.
        # Deswegen my_task_type.status_model anstelle von my_status_model.
        set_status(my_task_type.status_model, obj.id, task_type_status)      

    return HttpResponseRedirect(reverse("tasks_notassigned"))

@login_required
def set_status_call(request, **kwargs):
    """
    View zum Status setzen, ohne Tasks. Benoetigte Argumente:

    model   = Modelname als String
    id      = id der Modelinstanz
    status  = status, der gesetzt werden soll
    """
    set_status(kwargs["model"], kwargs["id"], kwargs["status"])
    my_model = GtModel.str_to_gtmodel(kwargs["model"])

    my_redirect_url = request.META.get('HTTP_REFERER')
    # Wenn PRODUKTIONSDIENSTLEISTUNG eine Warenentnahme Richtung PRODUKTION macht
    # wird der Status entsprechend gesetzt und danach auf die manufacturing_list umgeleitet
    if my_model == CustOrderDet:
        if request.user.groups.filter(name=PRODUKTIONSDIENSTLEISTUNG).exists():
            if kwargs["status"] == int(CustOrderDet.Status.AUFTRAG_FREIGEGEBEN):
                my_redirect_url = reverse("manufacturing_list")
    
    # Wenn Lieferant eine Warenentnahme macht wird auf supp_order umgeleitet
    elif my_model == SuppOrder:
        if request.user.groups.filter(name=LIEFERANTEN).exists():
            if kwargs["status"] == int(SuppOrder.Status.GELIEFERT):
                my_redirect_url = reverse("supp_order")     

    return HttpResponseRedirect(my_redirect_url)

def set_status(model: str, id: int, status: int):
    """
    Keine View. Interne Methode zum setzen des Status. Benoetigte Argumente:
    """
    my_model = GtModel.str_to_gtmodel(model)
    my_obj = my_model.objects.get(id=id)
    # Nur Status aendern, wenn ein vernuenftiger Status > -1 uebergeben wird
    # Und wenn der Status groesser ist als der bisherige!
    if int(status) > UNKNOWN and int(my_obj.status) < int(status):
        #Custorder achtung dieser wird für die Freigabe des Auftrags verwendet SONST wird nur mit CustOrderDet gearbeitet
        if my_model == CustOrder:
            CustOrderDet.objects.filter(cust_order_id=id).update(status=status)
        else:
            my_model.objects.filter(id=id).update(status=status)