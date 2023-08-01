
import time
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from core.models import Subscriber
from django.conf import settings

class Command(BaseCommand):
    help = 'Send weekly emails to subscribers'

    def handle(self, *args, **kwargs):
        while True:
            subscribers = Subscriber.objects.all()
            print("while olan yer //////////////////////////////////////////////")
            for subscriber in subscribers:
                subject = 'Yenə mən'
                message = 'Bu mənim cv-min son halıdır. Ümid edirəm bu yolda mənə dəstək olarsız. Olmasanız mən sizin ömrünüzdən çıxmayacam'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [subscriber.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            # Wait for one week before sending emails again
            time.sleep(100)  # 604800 seconds = 1 week
