from . import *

#Status setzen
@login_required
def set_status_task (request, **kwargs):
    
    set_status(kwargs["id"], kwargs["type"], kwargs["status"])
    #custorder
    if kwargs["type_for_task"] == 1:
        Task.set_task_cust(CustOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custorderdet
    elif kwargs["type_for_task"] == 2:
        Task.set_task_cust_det(CustOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #supporder
    elif kwargs["type_for_task"] == 3:
        Task.set_task_supp(SuppOrder.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #supporderdet
    elif kwargs["type_for_task"] == 4:
        Task.set_task_supp_det(SuppOrderDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custcomplaint
    elif kwargs["type_for_task"] == 5:
        Task.set_task_custComplaint(CustComplaint.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #custcomplaintdet
    elif kwargs["type_for_task"] == 6:
        Task.set_task_custComplaintDet(CustComplaintDet.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    #suppcomplaint
    elif kwargs["type_for_task"] == 7:
        Task.set_task_suppComplaint(SuppComplaint.objects.get(id=kwargs["id"]), kwargs["tasktype"], Timers.get_current_day())
    else:
        pass
    return HttpResponseRedirect(reverse("tasks_notassigned"))


#Status und Task setzten, Da für jede Position ein Task angelegt werden muss, gibt es hier eine spezielle Funktion dafür
# Durchläuft alle Positionen
@login_required
def set_status_task_share (request, **kwargs):
    #custcomplaint freigegeben auf custcomplaintdet (Auftragsfreigabe Reklamationen)
    if kwargs["type_for_task"] == 6:
        mylist = list(CustComplaintDet.objects.filter(cust_complaint_id = kwargs["id"])) 
        for i in mylist:
            set_status(i.id, kwargs["type"], kwargs["status"])
            Task.set_task_custComplaintDet(i,kwargs["tasktype"],Timers.get_current_day())
    elif kwargs["type_for_task"] == 1: 
        mylist = list(CustOrderDet.objects.filter(cust_order_id = kwargs["id"]))  
        set_status(kwargs["id"], kwargs["type"], kwargs["status"])
        for i in mylist:
            Task.set_task_cust_det(i, kwargs["tasktype"], Timers.get_current_day())
    return HttpResponseRedirect(reverse("tasks_notassigned"))


# Status setzen bei Auftrag freigeben
@login_required
def set_status_call(request, **kwargs):
    set_status(kwargs["id"], kwargs["type"], kwargs["status"])

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #return HttpResponseRedirect(reverse("home"))


#Status setzen keine view
def set_status(id, type, status):
    #custorder achtung dieser wird für die Freigabe des Auftrags verwendet SONST wird nur mit CustOrderDet gearbeitet
    if type == 1:
        mylist = list(CustOrderDet.objects.filter(cust_order_id = id))
        for i in mylist:
            CustOrderDet.objects.filter(pk=i.id).update(status=status)
    #custorderdet
    elif type == 2:
        CustOrderDet.objects.filter(pk=id).update(status=status)
    #supporder
    elif type == 3:
        SuppOrder.objects.filter(pk=id).update(status=status)
    #supporderdet
    elif type == 4:
        SuppOrderDet.objects.filter(pk=id).update(status=status)
    elif type == 5:
        CustComplaint.objects.filter(pk=id).update(status=status)
    elif type == 6:
        CustComplaintDet.objects.filter(pk=id).update(status=status)
    elif type == 7:
        SuppComplaint.objects.filter(pk=id).update(status=status)
    elif type == 8:
        SuppComplaintDet.objects.filter(pk=id).update(status=status)
    else:
        pass
    