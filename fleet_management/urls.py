"""
URL configuration for fleet_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from fleet import views
from fleet.models import report_detail
from fleet.views import service_history_list, edit_email_template, send_notification

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/new/', views.driver_create, name='driver_create'),
    path('drivers/<int:pk>/edit/', views.driver_update, name='driver_update'),
    path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),

    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/new/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),

    path('servicehistory/new/', views.create_service_history, name='create_service_history'),
    path('servicehistory/<int:pk>/edit/', views.service_history_update, name='service_history_update'),
    path('servicehistory/<int:pk>/delete/', views.service_history_delete, name='service_history_delete'),
    path('servicehistory/', views.service_history_list, name='service_history_list'),

    path('edit_email_template/', edit_email_template, name='edit_email_template'),
    path('send_notification/<int:service_id>/', send_notification, name='send_notification'),

    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.create_report, name='create_report'),
    path('reports/<int:report_id>/', views.view_report, name='view_report'),
    path('reports/<int:report_id>/', report_detail, name='report_detail')
]

