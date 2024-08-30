# fleet/management/commands/check_service_dates.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from fleet.models import ServiceHistory
from fleet.tasks import send_service_notification

class Command(BaseCommand):
    help = 'Check for upcoming service dates and send notifications'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        upcoming_services = ServiceHistory.objects.filter(
            next_service_date=today + timedelta(days=30)
        )
        for service in upcoming_services:
            send_service_notification.delay(service.id)
        self.stdout.write(self.style.SUCCESS('Successfully checked for upcoming services and sent notifications.'))
