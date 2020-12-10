from django.urls import path, include
from gtapp.views import change_user_view, change_user_to_view
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_list_notassigned_view
from gtapp.views import cust_order_list_view, cust_order_alter_view, cust_order_create_view

urlpatterns = [
    path('', home_view, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_user/', change_user_view, name='change_user'),
    path('accounts/change_user/<int:id>/', change_user_to_view, name='change_user_to'),
    path('tasks/', tasks_view, name='tasks'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='tasks_assigned'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='tasks_notassigned'),
    path('CustOrder_list/', cust_order_list_view, name='custorder_list'),
    path('CustOrder_create/', cust_order_create_view, name='custorder_create'),
    path('CustOrder_alter/<int:id>/', cust_order_alter_view, name='custorder_alter'),
]