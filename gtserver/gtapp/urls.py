from django.urls import path, include
from gtapp.views import *

urlpatterns = [
    # von Häufig nach selten
    
    # API Status zuerst, da sie alle X Sekunden aufgerufen wird
    path('api/status/', get_api_status, name="api_status"),
    path('api/tasks/', get_api_tasks, name="api_tasks"),

    # Startseite
    path('', home_view, name='home'),
    path('home_information_pages/<str:info>/', home_information_pages.as_view(), name="home_information_pages"),
    path('faq/<int:content>/', faq_view.as_view(), name='faq'),

    # Login, Logout, Change User
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/change_user/', change_user_view, name='change_user'),
    path('accounts/change_user/<int:id>/', change_user_to_view, name='change_user_to'),

    # Aufgaben
    path('tasks/', tasks_view, name='tasks'),
    path('tasks_list/assigned/', tasks_list_assigned_view, name='tasks_assigned'),
    path('tasks_list/notassigned/', tasks_list_notassigned_view, name='tasks_notassigned'),
    path('tasks_list/finished/', tasks_list_finished_view, name='tasks_finished'),
    path('tasks_detail/<int:id>/', Tasks_detail_view.as_view(), name='tasks_detail'),
    path('tasks_assign/<int:id>/', tasks_assign_to_me_view, name='tasks_assign'),
    path('tasks_share/<int:id>/', tasks_share_to_team_view, name='tasks_share'),
    path('tasks_edit/<int:id>/', tasks_edit, name='tasks_edit'),
    path('tasks_finish/<int:id>/', tasks_finish, name='tasks_finish'),

    # Nachrichten
    path('msg/inbox/', inboxView.as_view(), name="inbox"),
    path('msg/outbox/', outboxView.as_view(), name='outbox'),
    path('msg/bin/', binView.as_view(), name='bin'),
    path('msg/write/', msgWriteView.as_view(), name='msgwrite'),
    path('msg/details/<int:id>/', msgDetailsView.as_view(), name='msgdetails'),
    path('msg/delete/<int:id>/', delete_message_view, name='msgdelete'),
    path('msg/api/<int:id>/', add_order_view, name='msgorderadd'),

    # Boxscan
    path('box/', box_view.as_view(), name="box_view"),
    path('box/<int:error>/', box_view.as_view(), name="box_view_error"),
    path('box_search/', box_search_view, name='box_search_view'),
    path('box_assign/<str:model>/<int:id>/', Box_assign_view.as_view(), name='box_assign'),

    # Task Status
    path('status_call/<str:model>/<int:id>/<int:status>/', set_status_call, name='set_status_call'),
    path('status_task/<int:id>/<int:task_type>/', set_status_task, name='set_status_task'),

    # Cust Order
    path('cust_order/', Cust_order_view.as_view(), name="cust_order"),
    path('cust_order/create/', Cust_order_create_view.as_view(), name='cust_order_create'),
    path('cust_order/alter/<int:id>/', Cust_order_alter_view.as_view(), name='cust_order_alter'),
    path('cust_order/delete/<int:id>/', Cust_order_delete_view.as_view(), name='cust_order_delete'),
    path('cust_order/cancel/<int:id>/', Cust_order_cancel_view.as_view(), name='cust_order_cancel'),
    path('cust_order_det/create/<int:cust_order>/', Cust_order_det_create_view.as_view(), name="cust_order_det_create"),
    path('cust_order_det/alter/<int:id>/', Cust_order_det_alter_view.as_view(), name="cust_order_det_alter"),
    path('cust_order_det/delete/<int:id>/', Cust_order_det_delete_view.as_view(), name="cust_order_det_delete"),
    path('cust_order_det/cancel/<int:id>/', Cust_order_det_cancel_view.as_view(), name="cust_order_det_cancel"),

    # Supp Order
    path('supp_order/', Supp_order_view.as_view(), name="supp_order"),
    path('supp_order/create/', Supp_order_create_view.as_view(), name='supp_order_create'),
    path('supp_order/alter/<int:id>/', Supp_order_alter_view.as_view(), name='supp_order_alter'),
    path('supp_order/delete/<int:id>/', Supp_order_delete_view.as_view(), name='supp_order_delete'),
    path('supp_order/cancel/<int:id>/', Supp_order_cancel_view.as_view(), name='supp_order_cancel'),
    path('supp_order_det/create/<int:supp_order>/', Supp_order_det_create_view.as_view(), name="supp_order_det_create"),
    path('supp_order_det/alter/<int:id>/', Supp_order_det_alter_view.as_view(), name="supp_order_det_alter"),
    path('supp_order_det/delete/<int:id>/', Supp_order_det_delete_view.as_view(), name="supp_order_det_delete"),

    # PDL
    path('manufacturing/', manufacturing_list_view, name="manufacturing_list"),
    path('manufacturing_complaints/', manufacturing_list_view, name="manufacturing_complaints"),
    path('manufacturing/release/<int:id>/', manufacturing_release_view, name="manufacturing_release"),
    path('manufacturing/supporder/<int:id>/', manufacturing_supporder_view, name="manufacturing_supporder"),
    #path('manufacturing/testing/<int:id>/', stock_check_view, name="manufacturing_testing"),
    
    # Lager
    path('stock/', stock_view, name="stock"),
    path('stock/alter/<int:id>/', Stock_alter_view.as_view(), name="stock_alter"),
    path('stock/movements/<int:id>/', StockmovementView.as_view(), name="stockmovement"),
    path('stock/check/<int:id>/', stock_check_view, name="stock_check"),

    # Wareneingang
    path('goods_receipt/<int:typeofdet>/<int:idofdet>/', goods_receipt_view, name="goods_receipt"),

    # Warenausgang
    path('goods_receipt/<str:model>/<int:id>/', delivery_view, name="goods_receipt"),
    path('goods_shipping/<str:model>/<int:id>/', delivery_view, name="goods_shipping"),
    #path('goods_shipping/<str:model>/<int:id>/', Delivery_create_view.as_view(), name="goods_shipping"),

    # Produktionsschritte
    path('production_steps/', production_steps, name="production_steps"),
    path('production_steps_single/<str:product>/<int:step>/', production_steps_single.as_view(), name="production_steps_single"),
    path('production_steps_3D_models/<str:product>/<int:step>/', production_steps_3D_models.as_view(), name="production_steps_3D_models"),

    # Cust Order Reklamation
    path('cust_complaint/', Cust_complaint_view.as_view(), name="cust_complaint"),
    path('cust_complaint/create/', Cust_complaint_create_view.as_view(), name='cust_complaint_create'),
    path('cust_complaint/alter/<int:id>/', Cust_complaint_alter_view.as_view(), name='cust_complaint_alter'),
    path('cust_complaint/delete/<int:id>/', Cust_complaint_delete_view.as_view(), name='cust_complaint_delete'),
    path('cust_complaint_det/create/<int:cust_complaint>/', Cust_complaint_det_create_view.as_view(), name="cust_complaint_det_create"),
    path('cust_complaint_det/alter/<int:id>/', Cust_complaint_det_alter_view.as_view(), name="cust_complaint_det_alter"),
    path('cust_complaint_det/delete/<int:id>/', Cust_complaint_det_delete_view.as_view(), name="cust_complaint_det_delete"),

    # Supp Order Reklamation
    path('supp_complaint/', Supp_complaint_view.as_view(), name="supp_complaint"),
    path('supp_complaint/create/', Supp_complaint_create_view.as_view(), name='supp_complaint_create'),
    path('supp_complaint/alter/<int:id>/', Supp_complaint_alter_view.as_view(), name='supp_complaint_alter'),
    path('supp_complaint/delete/<int:id>/', Supp_complaint_delete_view.as_view(), name='supp_complaint_delete'),
    path('supp_complaint_det/create/<int:supp_complaint>/', Supp_complaint_det_create_view.as_view(), name="supp_complaint_det_create"),
    path('supp_complaint_det/alter/<int:id>/', Supp_complaint_det_alter_view.as_view(), name="supp_complaint_det_alter"),
    path('supp_complaint_det/delete/<int:id>/', Supp_complaint_det_delete_view.as_view(), name="supp_complaint_det_delete"),

]
