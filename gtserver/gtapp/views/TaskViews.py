from . import *

# Task Schaltfläche
@login_required
def tasks_view(request):
    c = get_context("Aufgaben", "Aufgaben")
    return render(request, "tasks.html", c)

# Zugewiesene Tasks View
@login_required
def tasks_list_assigned_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    c['tasks'] = Task.objects.filter(user=request.user, active=1)
    c['Headline'] = "Mir zugewiesene Aufgaben"
    c['assigned'] = 1
    return render(request, "tasks_list.html", c)

# Nicht-zugewiesene Tasks View
@login_required
def tasks_list_notassigned_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    myList = list()
    u = request.user.groups.all()
    for group in u:
        for i in Task.objects.filter(task_type__in=TaskType.objects.filter(group=group), user__isnull=True):
            myList.append(i)
    c["tasks"] = myList
    c['Headline'] = "Verfügbare Aufgaben"
    c['notassigned'] = 1
    return render(request, "tasks_list.html", c)

# Bearbeitete Tasks View
@login_required
def tasks_list_finished_view(request):
    c = get_context("Zugewiesene Aufgaben", "Aufgaben")
    c['tasks'] = Task.objects.filter(user=request.user, active=0)
    c['Headline'] = "Abgeschlossene Aufgaben"
    c['finished'] = 1
    return render(request, "tasks_list.html", c)

# Weise Task User zu
@login_required
def tasks_assign_to_me_view(request, **kwargs):
    Task.objects.filter(pk=kwargs["id"]).update(user=request.user)
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Weise Task Team zu
@login_required
def tasks_share_to_team_view(request, **kwargs):
    Task.objects.filter(pk=kwargs["id"]).update(user_id = '')
    return HttpResponseRedirect(reverse("tasks_assigned"))

# Beende Task
@login_required
def tasks_finish(request, **kwargs):
    
    Task.objects.filter(pk=kwargs["id"]).update(active=0, finished_on=Timers.get_current_day())
    return HttpResponseRedirect(reverse("tasks_finished"))
    

# Bearbeite Task
@login_required
def tasks_edit(request, **kwargs):
    mytask = Task.objects.filter(pk=kwargs["id"]).first()
    if mytask.task_type_id in [1, 16, 17, 18]:#==1 or mytask.task_type_id == 16 or mytask.task_type_id == 17 or mytask.task_type_id == 18:
        return HttpResponseRedirect(reverse("cust_order_alter", kwargs={'id':mytask.cust_order.pk}))
    elif mytask.task_type_id == 2:
        #Bestandsprüfungsseite eintragen
        pass
    elif mytask.task_type_id in [8]:
        my_cust_order = CustOrderDet.objects.get(id=mytask.cust_order_det.pk).cust_order.id
        return HttpResponseRedirect(reverse("cust_order_alter", kwargs={'id':my_cust_order}))
    elif mytask.task_type_id in [7]:
        return HttpResponseRedirect(reverse("manufacturing_list"))
    elif mytask.task_type_id in [19, 20]:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytask.supp_order.pk}))
    elif mytask.task_type_id in [9]:
        return HttpResponseRedirect(reverse("supp_order"))
    elif mytask.task_type_id == 20:
        return HttpResponseRedirect(reverse("supp_order_alter", kwargs={'id':mytask.supp_order.pk}))
    elif mytask.task_type_id == 21:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id == 22:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id == 23:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.pk}))
    elif mytask.task_type_id in [24,25,26]:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint_det.cust_complaint.pk}))
    elif mytask.task_type_id == 27:
        return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint_det.cust_complaint.pk}))
    elif mytask.task_type_id == 28:
        return HttpResponseRedirect(reverse("cust_complaint_det_alter", kwargs={'id':mytask.cust_complaint_det.cust_complaint.pk}))
    elif mytask.task_type_id == 29:
         return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint_det.cust_complaint.pk}))
    elif mytask.task_type_id == 32:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 33:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 34:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 35:
        return HttpResponseRedirect(reverse("supp_complaint_alter", kwargs={'id':mytask.supp_complaint.pk}))
    elif mytask.task_type_id == 36:
        #Bestandsprüfung einbauen
        pass



# Task Detail View
class Tasks_detail_view(LoginRequiredMixin, DetailView):
    template_name = "tasks_detail.html"
    model = Task


      # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = Task.objects.get(id=self.kwargs['id'])
        return obj