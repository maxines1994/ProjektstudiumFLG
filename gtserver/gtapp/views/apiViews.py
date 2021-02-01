from django.http import JsonResponse
from gtapp.models import Todo, TodoType
#from gtapp.constants import *
from gtapp.models import Timers

# Status alle x Sekunden (Tag, hatBenachrichtigungen)
def get_api_status(request, **kwargs):
    time = Timers.get_current_day()
    has_unassigned = Todo.has_unassigned(request.user)
    return JsonResponse(dict(time=time, has_unassigned=has_unassigned))

# Tasks laden
def get_api_tasks(request, **kwargs):

    tasks_user = list()
    for index, task in enumerate(Todo.get_tasks_of_user(request.user)):
        tasks_user.append(dict(id=task.id, title=task.todo_type.title_de, ref=task.get_ref()))

    tasks_group = list()
    for index, task in enumerate(Todo.get_unassigned_tasks(request.user)):
        tasks_group.append(dict(id=task.id, title=task.todo_type.title_de, ref=task.get_ref()))

    return JsonResponse(dict(tasks_user=tasks_user, tasks_group=tasks_group))



