from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from fleet.models import ServiceHistory
from datetime import timedelta

class Command(BaseCommand):
    help = 'Send notifications for upcoming service dates'

    def handle(self, *args, **kwargs):
        # Отримуємо поточну дату
        today = timezone.now().date()

        # Визначаємо дату через рік
        one_year_from_now = today + timedelta(days=365)

        # Отримуємо записи, які мають наступне обслуговування через рік
        services = ServiceHistory.objects.filter(next_service_date=one_year_from_now)

        for service in services:
            self.send_notification(service)

    def send_notification(self, service):
        subject = f"Reminder: {service.vehicle} needs service on {service.next_service_date}"
        message = f"Vehicle {service.vehicle} is scheduled for service on {service.next_service_date}. Please take action."
        recipient_list = ['recipient@example.com']  # Список отримувачів

        send_mail(subject, message, 'sender@example.com', recipient_list)
        self.stdout.write(f'Notification sent for {service.vehicle} - Next service date: {service.next_service_date}')

