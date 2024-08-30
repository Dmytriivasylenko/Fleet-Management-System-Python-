from datetime import timedelta, datetime
from time import timezone
from django.core.mail import send_mail
from .tasks import send_service_notification
from django.shortcuts import render, get_object_or_404, redirect
from fleet_management import settings
from .models import Driver, Vehicle, ServiceHistory, Report
from .forms import DriverForm, VehicleForm, ServiceHistoryForm, EmailTemplateForm, ReportForm


def home(request):
    return render(request, 'home_page.html')
def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'driver_list.html', {'drivers': drivers})

def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'driver_form.html', {'form': form})

def driver_update(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'driver_form.html', {'form': form})

def driver_delete(request, pk):
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        driver.delete()
        return redirect('driver_list')
    return render(request, 'driver_confirm_delete.html', {'driver': driver})

##########################VEHICLE#############################

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_form.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicle_form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})



########################SERVISHISTORY######################

def create_service_history(request):
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST)
        if form.is_valid():
            service_history = form.save()

            if service_history.next_service_date and service_history.next_service_date > datetime.now().date():
                send_service_reminder(service_history.vehicle, service_history.next_service_date)

            return redirect('service_history_list')
    else:
        form = ServiceHistoryForm()

    return render(request, 'service_history_form.html', {'form': form})

def service_history_update(request, pk):
    service_history = get_object_or_404(ServiceHistory, pk=pk)
    if request.method == 'POST':
        form = ServiceHistoryForm(request.POST, instance=service_history)
        if form.is_valid():
            form.save()
            return redirect('service_history_list')
    else:
        form = ServiceHistoryForm(instance=service_history)
    return render(request, 'service_history_form.html', {'form': form})

def service_history_delete(request, pk):
    service_history = get_object_or_404(ServiceHistory, pk=pk)
    if request.method == 'POST':
        service_history.delete()
        return redirect('service_history_list')
    return render(request, 'service_history_confirm_delete.html', {'service_histories': service_history})

def service_history_list(request):
    today = datetime.now()
    upcoming_services = ServiceHistory.objects.filter(next_service_date__lte=today + timedelta(days=7))

    service_histories = ServiceHistory.objects.all()
    return render(request, 'service_history_list.html', {
        'service_histories': service_histories,
        'upcoming_services': upcoming_services,
    })


def send_service_reminder(vehicle, upcoming_service_date):
    subject = 'Upcoming Service Reminder'
    message = f'This is a reminder that the next service for vehicle {vehicle} is due on {upcoming_service_date}.'
    recipient_list = ['recipient@example.com']

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

##################
def edit_email_template(request):
    if request.method == 'POST':
        form = EmailTemplateForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            ##################
            return redirect('service_history_list')
    else:
        form = EmailTemplateForm()
    return render(request, 'edit_email_template.html', {'form': form})


#NOT WORKING
def send_notification(request, service_id):
    service = get_object_or_404(ServiceHistory, id=service_id)
    send_service_notification.delay(service.id)
    return redirect('service_history_list')


def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save()
            return redirect('view_report', report_id=report.id)
    else:
        form = ReportForm()

    return render(request, 'create_report.html', {'form': form})



def view_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report_data = report.generate_report()

    return render(request, 'view_report.html', {'report': report, 'report_data': report_data})

def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports': reports})

def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'report_detail.html', {'report': report})
