from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from config.settings import EMAIL_HOST_USER
from lessons.models import Course, Subscription


@shared_task
def check_inactive_users():
    user = get_user_model()
    inactive_users = user.objects.filter(
        last_login__date__lte=timezone.now() - timedelta(days=30), is_active=True
    )
    for user in inactive_users:
        user.is_active = False
        user.save()


@shared_task
def subscription_update(pk):
    course = get_object_or_404(Course, pk=pk)
    subscriptions = Subscription.objects.filter(course_subscription=pk)
    subscribers = [subscription.user_subscription for subscription in subscriptions]
    for subscriber in subscribers:
        try:
            send_mail(
                subject="Подписка на курс",
                message=f'Добрый день, курс "{course.name}" был обновлен',
                from_email=EMAIL_HOST_USER,
                recipient_list=[
                    subscriber.email,
                ],
                # recipient_list=[EMAIL_HOST_USER, ],
            )
        except Exception as e:
            print(str(e))
