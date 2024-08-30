# fleet/urls.py

from django.urls import path
from . import views
from .views import edit_email_template, send_notification

urlpatterns = [
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/new/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/edit/', views.driver_update, name='driver_update'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/new/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),

    path('servicehistory/', views.service_history_list, name='service_history_list'),
    path('servicehistory/new/', views.service_history_update, name='service_history_create'),
    path('servicehistory/<int:pk>/edit/', views.service_history_update, name='service_history_update'),
    path('servicehistory/<int:pk>/delete/', views.service_history_delete, name='service_history_delete'),

    path('send_notification/<int:service_id>/', views.send_notification, name='send_notification'),
    path('edit_email_template/', edit_email_template, name='edit_email_template'),
    path('send_notification/<int:service_id>/', send_notification, name='send_notification'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:report_id>/', views.view_report, name='view_report'),

]
