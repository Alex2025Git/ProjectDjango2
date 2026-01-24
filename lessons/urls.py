from django.urls import path

from lessons.apps import LessonsConfig
from lessons.views import (LessonCreateAPIView, LessonDestroyAPIView,
                           LessonListAPIView, LessonRetrieveAPIView,
                           LessonUpdateAPIView)

app_name = LessonsConfig.name

urlpatterns = [
    path("", LessonListAPIView.as_view(), name="lesson-list"),
    path("<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path("create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
]
