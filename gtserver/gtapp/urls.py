from django.urls import path, include
from gtapp.views import change_user_view, change_user_to_view, get_api_status, get_api_tasks
from gtapp.views import binView, inboxView, outboxView, msgWriteView, delete_message_view, msgDetailsView, add_order_view
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_edit,tasks_finish, tasks_list_finished_view, tasks_list_notassigned_view, Cust_order_create_view, Cust_order_alter_view, Cust_order_det_create_view, Cust_order_det_alter_view, Cust_order_view, Cust_order_det_delete_view, Cust_order_delete_view, Tasks_detail_view, tasks_assign_to_me_view, tasks_share_to_team_view
from gtapp.views.stdViews import home_information_pages
from gtapp.views.ProductionViews import production_steps, production_steps_single, production_steps_3D_models
from gtapp.views.CustComplaintViews import Cust_complaint_view, Cust_complaint_create_view, Cust_complaint_alter_view, Cust_complaint_delete_view, Cust_complaint_det_create_view, Cust_complaint_det_alter_view, Cust_complaint_det_delete_view
from gtapp.views.SuppOrderViews import Supp_order_view, Supp_order_create_view, Supp_order_alter_view, Supp_order_delete_view, Supp_order_det_create_view, Supp_order_det_alter_view, Supp_order_det_delete_view
from gtapp.views.SuppComplaintViews import Supp_complaint_view, Supp_complaint_create_view, Supp_complaint_alter_view, Supp_complaint_delete_view, Supp_complaint_det_create_view, Supp_complaint_det_alter_view, Supp_complaint_det_delete_view
from gtapp.views import manufacturing_list_view, manufacturing_release_view, manufacturing_supporder_view, manufacturing_testing_view, manufacturing_stock_view

urlpatterns = [
    path('', home_view, name='home'),
    path('home_information_pages/<str:info>/', home_information_pages.as_view(), name="home_information_pages"),

    path('api/status/', get_api_status, name="api_status"),
    path('api/tasks/', get_api_tasks, name="api_tasks"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_user/', change_user_view, name='change_user'),
    path('accounts/change_user/<int:id>/', change_user_to_view, name='change_user_to'),

    path('msg/inbox/', inboxView.as_view(), name="inbox"),
    path('msg/outbox/', outboxView.as_view(), name='outbox'),
    path('msg/bin/', binView.as_view(), name='bin'),
    path('msg/write/', msgWriteView.as_view(), name='msgwrite'),
    path('msg/details/<int:id>/', msgDetailsView.as_view(), name='msgdetails'),
    path('msg/delete/<int:id>/', delete_message_view, name='msgdelete'),
    path('msg/api/<int:id>/', add_order_view, name='msgorderadd'),

    path('tasks/', tasks_view, name='tasks'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='tasks_assigned'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='tasks_notassigned'),
    path('tasks_list/finished/', tasks_list_finished_view, name='tasks_finished'),
    path('tasks_detail/<int:id>/', Tasks_detail_view.as_view(), name='tasks_detail'),
    path('tasks_assign/<int:id>/', tasks_assign_to_me_view, name='tasks_assign'),
    path('tasks_share/<int:id>/', tasks_share_to_team_view, name='tasks_share'),
    path('tasks_edit/<int:id>/', tasks_edit, name='tasks_edit'),
    path('tasks_finish/<int:id>/', tasks_finish, name='tasks_finish'),

    path('cust_order/', Cust_order_view.as_view(), name="cust_order"),
    path('cust_order/create/', Cust_order_create_view.as_view(), name='cust_order_create'),
    path('cust_order/alter/<int:id>/', Cust_order_alter_view.as_view(), name='cust_order_alter'),
    path('cust_order/delete/<int:id>/', Cust_order_delete_view.as_view(), name='cust_order_delete'),

    path('cust_order_det/create/<int:cust_order>/', Cust_order_det_create_view.as_view(), name="cust_order_det_create"),
    path('cust_order_det/alter/<int:id>/', Cust_order_det_alter_view.as_view(), name="cust_order_det_alter"),
    path('cust_order_det/delete/<int:id>/', Cust_order_det_delete_view.as_view(), name="cust_order_det_delete"),

    path('production_steps', production_steps, name="production_steps"),
    path('production_steps_single/<str:product>/<int:step>', production_steps_single.as_view(), name="production_steps_single"),
    path('production_steps_3D_models/<str:product>/<int:step>', production_steps_3D_models.as_view(), name="production_steps_3D_models"),
    
    path('cust_complaint/', Cust_complaint_view.as_view(), name="cust_complaint"),
    path('cust_complaint/create/', Cust_complaint_create_view.as_view(), name='cust_complaint_create'),
    path('cust_complaint/alter/<int:id>/', Cust_complaint_alter_view.as_view(), name='cust_complaint_alter'),
    path('cust_complaint/delete/<int:id>/', Cust_complaint_delete_view.as_view(), name='cust_complaint_delete'),

    path('cust_complaint_det/create/<int:cust_complaint>/', Cust_complaint_det_create_view.as_view(), name="cust_complaint_det_create"),
    path('cust_complaint_det/alter/<int:id>/', Cust_complaint_det_alter_view.as_view(), name="cust_complaint_det_alter"),
    path('cust_complaint_det/delete/<int:id>/', Cust_complaint_det_delete_view.as_view(), name="cust_complaint_det_delete"),

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
    path('supp_complaint_det/delete/<int:id>/', Supp_complaint_det_delete_view.as_view(), name="supp_complaint_det_delete"),

    path('manufacturing/', manufacturing_list_view, name="manufacturing_list"),
    path('manufacturing/release/<int:id>/', manufacturing_release_view, name="manufacturing_release"),
    path('manufacturing/supporder/<int:id>/', manufacturing_supporder_view, name="manufacturing_supporder"),
    path('manufacturing/testing/<int:id>/', manufacturing_testing_view, name="manufacturing_testing"),
    path('manufacturing/stock/', manufacturing_stock_view, name="manufacturing_stock"),
]
