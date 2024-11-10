from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_form, name='borrow_return_form'),
    path("staff_list_search/", views.form_search_staff, name="staff_search"),
    path("equipment_list_search/", views.form_search_equipment, name="equipment_search"),
    path('telegram_bot/', views.telegram_update, name='telegram_bot'),
    path('list/',views.employee_list,name="employee_list"),
    path('ajax_list/',view=views.getJson,name='employee_list_ajax'),
    path('staff/',view=views.employee_staff,name='staff_list'),
    path('staff_list/',view=views.staffJson,name='staff_list_ajax'),
    path('equipment/',view=views.employee_equipment,name='equipment_list'),
    path('equipment_list/',view=views.equipmentJson,name='equipment_list_ajax'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path("clear_all_data_list/", views.clear_all_data_list, name="clear_all_data_list"),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('edit_staff/<int:id>/', views.edit_staff, name='edit_staff'),
    #path('delete_staff/<int:id>/', views.delete_staff, name='delete_staff'),
    path('delete_multiple/', views.delete_multiple, name='delete_multiple'),
    path("clear_all_data/", views.clear_all_data, name="clear_all_data"),
    path('import_csv/', views.import_csv, name='import_csv'),
    path('add_equipment/', views.add_equipment, name='add_equipment'),
    path('edit_equipment/<int:id>/', views.edit_equipment, name='edit_equipment'),
    path('delete_multiple_equipment/', views.delete_multiple_equipment, name='delete_multiple_equipment'),
    path("clear_all_data_equipment/", views.clear_all_data_equipment, name="clear_all_data_equipment"),
    path('import_csv_equipment/', views.import_csv_equipment, name='import_csv_equipment'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
]   