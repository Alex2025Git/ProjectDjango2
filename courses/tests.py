from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from lessons.models import Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@admin.com", password="1234")
        self.course = Course.objects.create(
            name="Новый курс", description="Описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Новый урок",
            description="Описание урока",
            owner=self.user,
            course=self.course,
            link_video="",
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("courses:course-detail", args=[self.course.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        url = reverse("courses:course-list")
        data = {
            "name": "Тестовый курс",
            "description": "Тестовое описание курса",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("courses:course-detail", args=[self.course.id])
        data = {
            "name": "Тестовый курс изменения",
            "description": "Тестовое описание курса",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тестовый курс изменения")

    def test_course_delete(self):
        url = reverse("courses:course-detail", args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("courses:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
