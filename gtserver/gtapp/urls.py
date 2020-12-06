from django.urls import path
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_list_notassigned_view
from gtapp.views import cust_order_list_view, cust_order_alter_view, cust_order_create_view

urlpatterns = [
    path('', home_view, name='home'),
    path('tasks/', tasks_view, name='home'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='home'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='home'),
    path('CustOrder_list/', cust_order_list_view, name='home'),
    path('CustOrder_create/', cust_order_create_view, name='home'),
    path('CustOrder_alter/<int:id>/', cust_order_alter_view, name='home'),
]