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
    return HttpResponseRedirect(reverse("tasks_assigned"))
    
# Bearbeite Task
@login_required
def tasks_edit(request, **kwargs):
    """
    Leitet den User zu der Seite auf der das Objekt des Tasks weiter bearbeitet werden kann
    """
    # Hole den Task
    mytask = Task.objects.filter(pk=kwargs["id"]).first()
    # Hole das Template, auf das weiter geleitet werden soll
    my_tasktype = TaskType.objects.get(id=mytask.id)
    my_view_url = TaskType.objects.get(id=mytask.task_type_id).view_url
    # Falls die Template Parameter erwartet: 
    if TaskType.objects.get(id=mytask.task_type_id).view_kwargs_id != '':
        # Hole den in TaskType.view_kwargs_id hinterlegten Feldnamen
        my_task_model_field = TaskType.objects.get(id=mytask.task_type_id).view_kwargs_id
        # Hol die id die bei diesem Feldnamen bei diesem Task hinterlegt ist (Z.b. die cust_order_det_id)
        my_task_model_id = getattr(mytask, my_task_model_field)
        # Baue einen Filter der zu uebergebenden Paramter an die View
        mykwargs = {}
        mykwargs['id'] = my_task_model_id
        # Redirect mit Parameter
        return HttpResponseRedirect(reverse(my_view_url, kwargs=mykwargs))
        # Ergebnisbeispiel mit fingierten Variablen:
        # return HttpResponseRedirect(reverse("cust_complaint_alter", kwargs={'id':mytask.cust_complaint.id}))
    else:
        # Redirect ohne Parameter
        return HttpResponseRedirect(reverse(my_view_url))

# Task Detail View
class Tasks_detail_view(LoginRequiredMixin, DetailView):
    template_name = "tasks_detail.html"
    model = Task


      # Objekt für Alter view getten
    def get_object(self, queryset=None):
        obj = Task.objects.get(id=self.kwargs['id'])
        return obj
    
    #Hier die TaskTypeId reinpacken zu welcher Tabelle sie Gehört
    #Dadurch wir die "Überschrift" auch richtig angezeigt
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["CustOrder"] = [1,16,17,18]
        context["CustOrderDet"] = [2,3,5,6,7,8,11,12,13]
        context["SuppOrder"] = [4,9,10,12,15,19,20]
        context["CustComplaint"] = [21,22,23]
        context["CustComplaintDet"] = [24,25,26,27,28,29,31]
        context["SuppComplaint"] = [32,33,34,35,36,37]
        #context["SuppComplaintDet"] = []
        return context