from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from lessons.models import Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@admin.com", password="1234")
        self.course = Course.objects.create(
            name="Новый курс", description="Описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Новый урок", description="Описание урока", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("lessons:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Урок 1",
            "description": "Описание урока 1",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_youtube(self):
        url = reverse("lessons:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Урок 1",
            "description": "Описание урока 1",
            "course": self.course.pk,
            "owner": self.user.pk,
            "link_video": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_no_youtube(self):
        url = reverse("lessons:lesson-create")
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "Урок 1",
            "description": "Описание урока 1",
            "course": self.course.pk,
            "owner": self.user.pk,
            "link_video": "https://www.test.ru/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_retrieve(self):
        url = reverse("lessons:lesson-retrieve", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        url = reverse("lessons:lesson-update", args=(self.lesson.pk,))
        data = {
            "name": "Урок 2",
            "description": "Описание урока 2",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок 2")

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lessons:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lessons:lesson-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="www@yandex.com")
        self.course = Course.objects.create(
            name="Курс 1", description="Описание курса 1", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Урок 1",
            description="Описание урок 1",
            course=self.course,
            owner=self.user,
        )
        self.subscription = Subscription.objects.create(
            user_subscription=self.user, course_subscription=self.course
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        Subscription.objects.all().delete()
        url = reverse("lessons:subscription-create")
        data = {"course_subscription": self.course.pk}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена!")
        self.assertTrue(
            Subscription.objects.filter(
                user_subscription=self.user, course_subscription=self.course
            ).exists()
        )
        url = reverse("lessons:subscription-create")
        data = {"course_subscription": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена!")

    def test_subscription_list(self):
        url = reverse("lessons:subscription-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course_subscription"], self.course.id)

    def test_subscribe_course_no_id(self):
        Subscription.objects.all().delete()
        url = reverse("lessons:subscription-create")
        data = {"course_id": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_course_no_auth(self):
        Subscription.objects.all().delete()
        self.client.force_authenticate(user="")
        url = reverse("lessons:subscription-create")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
