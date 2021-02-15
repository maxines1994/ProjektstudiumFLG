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
    my_filter = {}
    # Ist der Flag "for_all_details" gesetzt, wird der hinterlegte Status und Task
    # fuer alle Positionsdaten angelegt. Daher lautet der Filter nicht "id = kwargs["id"]"
    # sondern "xxx_order = kwargs["id"]" oder "xxx_complaint = kwargs["id"]"
    if my_task_type.for_all_details:
        my_header_model = GtModel.str_to_gtmodel(my_task_type.task_model.replace('Det', ''))
        my_header_field = GtModel.gtmodel_to_foreign_field_name(my_header_model)
        my_filter[my_header_field] = kwargs["id"]
    else:
        my_filter["id"] = kwargs["id"]
    
    # Query aller gefundenen Objekte
    my_obj_qry = my_task_model.objects.filter(**my_filter)

    # Durchlaeuft das Query der gefundenen Objekte und setzt fuer jedes Objekt einen Task.
    for obj in my_obj_qry:
        # An set_status muss das Model wieder als String uebergeben werden.
        # Deswegen my_task_type.status_model anstelle von my_status_model.
        set_status(my_task_type.status_model, obj.id, task_type_status)
        Task.set_task(obj=obj, task_type_id=kwargs["task_type"])

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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def set_status(model: GtModel, id: int, status: int):
    """
    Keine View. Interne Methode zum setzen des Status. Benoetigte Argumente:
    """
    # Nur Status aendern, wenn ein vernuenftiger Status > -1 uebergeben wird.
    if int(status) > UNKNOWN:
        my_model = GtModel.str_to_gtmodel(model)
        #Custorder achtung dieser wird für die Freigabe des Auftrags verwendet SONST wird nur mit CustOrderDet gearbeitet
        if my_model == CustOrder:
            CustOrderDet.objects.filter(cust_order_id=id).update(status=status)
        else:
            my_model.objects.filter(id=id).update(status=status)