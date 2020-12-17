from django.urls import path, include
from gtapp.views import change_user_view, change_user_to_view
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_list_notassigned_view
from gtapp.views.CustOrderViews import Cust_order_create_view, Cust_order_alter_view, Cust_order_det_create_view, Cust_order_det_alter_view, Cust_order_view, Cust_order_det_delete_view, Cust_order_delete_view
from gtapp.views.SuppOrderViews import Supp_order_create_view, Supp_order_alter_view, Supp_order_det_create_view, Supp_order_det_alter_view, Supp_order_view, Supp_order_det_delete_view, Supp_order_delete_view


urlpatterns = [
    path('', home_view, name='home'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_user/', change_user_view, name='change_user'),
    path('accounts/change_user/<int:id>/', change_user_to_view, name='change_user_to'),

    path('tasks/', tasks_view, name='tasks'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='tasks_assigned'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='tasks_notassigned'),

    path('cust_order/', Cust_order_view.as_view(), name="cust_order"),
    path('cust_order/create/', Cust_order_create_view.as_view(), name='cust_order_create'),
    path('cust_order/alter/<int:id>/', Cust_order_alter_view.as_view(), name='cust_order_alter'),
    path('cust_order/delete/<int:id>/', Cust_order_delete_view.as_view(), name='cust_order_delete'),

    path('cust_order_det/create/<int:cust_order>/', Cust_order_det_create_view.as_view(), name="cust_order_det_create"),
    path('cust_order_det/alter/<int:id>/', Cust_order_det_alter_view.as_view(), name="cust_order_det_alter"),
    path('cust_order_det/delete/<int:id>/', Cust_order_det_delete_view.as_view(), name="cust_order_det_delete"),

    path('supp_order/', Supp_order_view.as_view(), name="supp_order"),
    path('supp_order/create/', Supp_order_create_view.as_view(), name='supp_order_create'),
    path('supp_order/alter/<int:id>/', Supp_order_alter_view.as_view(), name='supp_order_alter'),
    path('supp_order/delete/<int:id>/', Supp_order_delete_view.as_view(), name='supp_order_delete'),

    path('supp_order_det/create/<int:cust_order>/', Supp_order_det_create_view.as_view(), name="supp_order_det_create"),
    path('supp_order_det/alter/<int:id>/', Supp_order_det_alter_view.as_view(), name="supp_order_det_alter"),
    path('supp_order_det/delete/<int:id>/', Supp_order_det_delete_view.as_view(), name="supp_order_det_delete")
]