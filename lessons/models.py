from django.db import models

from courses.models import Course


class Lesson(models.Model):
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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
