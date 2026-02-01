from django.db import models

from config import settings


class Course(models.Model):
    """Описание модели по курсам"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(
        null=True, blank=True, upload_to="blog/photos", verbose_name="Превью"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name
