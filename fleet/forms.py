
from django import forms
from .models import Driver, Vehicle, ServiceHistory, Report


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'phone_number', 'assigned_car']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'


class ServiceHistoryForm(forms.ModelForm):
    class Meta:
        model = ServiceHistory
        fields = ['vehicle', 'service_date', 'service_type', 'cost', 'notes', 'next_service_date']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'next_service_date': forms.DateInput(attrs={'type': 'date'}),
            'cost': forms.NumberInput(attrs={'step': '0.01'}),
        }
    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.all(),
        empty_label="Select a vehicle"
    )

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['vehicle', 'driver', 'start_date', 'end_date', 'include_service_history', 'include_costs']


class EmailTemplateForm(forms.Form):
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message body'}))
