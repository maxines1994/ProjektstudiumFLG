from django.urls import path, include
from gtapp.views import change_user_view, change_user_to_view, get_async_information
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_list_notassigned_view, Cust_order_create_view, Cust_order_alter_view, Cust_order_det_create_view, Cust_order_det_alter_view, Cust_order_view, Cust_order_det_delete_view, Cust_order_delete_view, Tasks_detail_view, tasks_assign_to_me_view, tasks_share_to_team_view
from gtapp.views.SuppOrderViews import Supp_order_view, Supp_order_create_view, Supp_order_alter_view, Supp_order_delete_view, Supp_order_det_create_view, Supp_order_det_alter_view, Supp_order_det_delete_view
from gtapp.views.SuppComplaintViews import Supp_complaint_view, Supp_complaint_create_view, Supp_complaint_alter_view, Supp_complaint_delete_view, Supp_complaint_det_create_view, Supp_complaint_det_alter_view, Supp_complaint_det_delete_view

urlpatterns = [
    path('', home_view, name='home'),

    path('api/', get_async_information, name="apicall"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_user/', change_user_view, name='change_user'),
    path('accounts/change_user/<int:id>/', change_user_to_view, name='change_user_to'),

    path('tasks/', tasks_view, name='tasks'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='tasks_assigned'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='tasks_notassigned'),
    path('tasks_detail/<int:pk>/', Tasks_detail_view.as_view(), name='tasks_detail'),
    path('tasks_assign/<int:id>/', tasks_assign_to_me_view, name='tasks_assign'),
    path('tasks_share/<int:id>/', tasks_share_to_team_view, name='tasks_share'),

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

    path('supp_order_det/create/<int:supp_order>/', Supp_order_det_create_view.as_view(), name="supp_order_det_create"),
    path('supp_order_det/alter/<int:id>/', Supp_order_det_alter_view.as_view(), name="supp_order_det_alter"),
    path('supp_order_det/delete/<int:id>/', Supp_order_det_delete_view.as_view(), name="supp_order_det_delete"),

    path('supp_complaint/', Supp_complaint_view.as_view(), name="supp_complaint"),
    path('supp_complaint/create/', Supp_complaint_create_view.as_view(), name='supp_complaint_create'),
    path('supp_complaint/alter/<int:id>/', Supp_complaint_alter_view.as_view(), name='supp_complaint_alter'),
    path('supp_complaint/delete/<int:id>/', Supp_complaint_delete_view.as_view(), name='supp_complaint_delete'),

    path('supp_complaint_det/create/<int:supp_complaint>/', Supp_complaint_det_create_view.as_view(), name="supp_complaint_det_create"),
    path('supp_complaint_det/alter/<int:id>/', Supp_complaint_det_alter_view.as_view(), name="supp_complaint_det_alter"),
    path('supp_complaint_det/delete/<int:id>/', Supp_complaint_det_delete_view.as_view(), name="supp_complaint_det_delete")
]
