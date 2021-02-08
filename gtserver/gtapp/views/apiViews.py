from django.http import JsonResponse
from gtapp.models import Task, TaskType
#from gtapp.constants import *
from gtapp.models import Timers
from django.contrib.auth.decorators import login_required

# Status alle x Sekunden (Tag, hatBenachrichtigungen)
@login_required
def get_api_status(request, **kwargs):
    time = Timers.get_current_day()
    has_unassigned = Task.has_unassigned(request.user)
    return JsonResponse(dict(time=time, has_unassigned=has_unassigned))

# Tasks laden
@login_required
def get_api_tasks(request, **kwargs):

    tasks_user = list()
    for index, task in enumerate(Task.get_tasks_of_user(request.user)):
        tasks_user.append(dict(id=task.id, title=task.task_type.title, ref=task.get_ref()))

    tasks_group = list()
    for index, task in enumerate(Task.get_unassigned_tasks(request.user)):
        tasks_group.append(dict(id=task.id, title=task.task_type.title, ref=task.get_ref()))

    return JsonResponse(dict(tasks_user=tasks_user, tasks_group=tasks_group))



