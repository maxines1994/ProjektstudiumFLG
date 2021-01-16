from django.urls import path, include
from gtapp.views import change_user_view, change_user_to_view, get_async_information
from gtapp.views import home_view, tasks_view, tasks_list_assigned_view, tasks_list_notassigned_view, Cust_order_create_view, Cust_order_alter_view, Cust_order_det_create_view, Cust_order_det_alter_view, Cust_order_view, Cust_order_det_delete_view, Cust_order_delete_view, Tasks_detail_view, tasks_assign_to_me_view, tasks_share_to_team_view
from gtapp.views.ProductionViews import Production_steps, M1_production_step_1, M1_production_step_2, M1_production_step_3, M1_production_step_4, M1_production_step_5, M1_production_step_6, M1_production_step_7, M1_production_step_8, M2_production_step_1, M2_production_step_2, M2_production_step_3, M2_production_step_4, M2_production_step_5, M2_production_step_6, M2_production_step_7, M2_production_step_8, M3_production_step_1, M3_production_step_2, M3_production_step_3, M3_production_step_4, M3_production_step_5, M3_production_step_6, M3_production_step_7, M3_production_step_8, M4_production_step_1, M4_production_step_2, M4_production_step_3, M4_production_step_4, M4_production_step_5, M4_production_step_6, M4_production_step_7, M4_production_step_8
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

    path('Production_steps', Production_steps, name="Production_steps"),
    path('M1_production_step_1', M1_production_step_1, name="M1_production_step_1"),
    path('M1_production_step_2', M1_production_step_2, name="M1_production_step_2"),
    path('M1_production_step_3', M1_production_step_3, name="M1_production_step_3"),
    path('M1_production_step_4', M1_production_step_4, name="M1_production_step_4"),
    path('M1_production_step_5', M1_production_step_5, name="M1_production_step_5"),
    path('M1_production_step_6', M1_production_step_6, name="M1_production_step_6"),
    path('M1_production_step_7', M1_production_step_7, name="M1_production_step_7"),
    path('M1_production_step_8', M1_production_step_8, name="M1_production_step_8"),
    path('M2_production_step_1', M2_production_step_1, name="M2_production_step_1"),
    path('M2_production_step_2', M2_production_step_2, name="M2_production_step_2"),
    path('M2_production_step_3', M2_production_step_3, name="M2_production_step_3"),
    path('M2_production_step_4', M2_production_step_4, name="M2_production_step_4"),
    path('M2_production_step_5', M2_production_step_5, name="M2_production_step_5"),
    path('M2_production_step_6', M2_production_step_6, name="M2_production_step_6"),
    path('M2_production_step_7', M2_production_step_7, name="M2_production_step_7"),
    path('M2_production_step_8', M2_production_step_8, name="M2_production_step_8"),
    path('M3_production_step_1', M3_production_step_1, name="M3_production_step_1"),
    path('M3_production_step_2', M3_production_step_2, name="M3_production_step_2"),
    path('M3_production_step_3', M3_production_step_3, name="M3_production_step_3"),
    path('M3_production_step_4', M3_production_step_4, name="M3_production_step_4"),
    path('M3_production_step_5', M3_production_step_5, name="M3_production_step_5"),
    path('M3_production_step_6', M3_production_step_6, name="M3_production_step_6"),
    path('M3_production_step_7', M3_production_step_7, name="M3_production_step_7"),
    path('M3_production_step_8', M3_production_step_8, name="M3_production_step_8"),
    path('M4_production_step_1', M4_production_step_1, name="M4_production_step_1"),
    path('M4_production_step_2', M4_production_step_2, name="M4_production_step_2"),
    path('M4_production_step_3', M4_production_step_3, name="M4_production_step_3"),
    path('M4_production_step_4', M4_production_step_4, name="M4_production_step_4"),
    path('M4_production_step_5', M4_production_step_5, name="M4_production_step_5"),
    path('M4_production_step_6', M4_production_step_6, name="M4_production_step_6"),
    path('M4_production_step_7', M4_production_step_7, name="M4_production_step_7"),
    path('M4_production_step_8', M4_production_step_8, name="M4_production_step_8")
]
