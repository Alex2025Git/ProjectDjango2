from django.db import models

from config import settings
from courses.models import Course


class Lesson(models.Model):
    """Описание модели по урокам"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(
        null=True, blank=True, upload_to="blog/photos", verbose_name="Превью"
    )
    link_video = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Класс подписки"""

    user_subscription = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    course_subscription = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )

    is_subscribed = models.BooleanField(default=False, verbose_name="Подписка")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return self.user_subscription
