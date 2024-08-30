from _pydatetime import timedelta
from datetime import datetime
from django.db import models
from django.shortcuts import get_object_or_404, render


class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=20)
    odometer_reading = models.IntegerField(default=0)



    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'


class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    assigned_car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class ServiceHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_history')
    service_date = models.DateField()
    service_type = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    next_service_date = models.DateField(null=True, blank=True)
    upcoming_service_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.next_service_date:
            self.next_service_date = self.service_date + timedelta(days=180)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.service_date} - {self.service_type} ({self.vehicle})'


class Report(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    include_service_history = models.BooleanField(default=True)
    include_costs = models.BooleanField(default=True)

    def __str__(self):
        return f"Report for {self.vehicle} and {self.driver} from {self.start_date} to {self.end_date}"


    class ReportGenerator:
        def __init__(self, vehicle, include_service_history=False, include_costs=False, start_date=None, end_date=None):
            self.vehicle = vehicle
            self.include_service_history = include_service_history
            self.include_costs = include_costs
            self.start_date = start_date
            self.end_date = end_date

    def generate_report(self):
        pass


def report_detail(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    return render(request, 'report_detail.html', {'report': report})