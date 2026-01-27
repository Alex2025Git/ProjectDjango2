from rest_framework.serializers import ModelSerializer

from lessons.models import Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор по урокам"""

    class Meta:
        model = Lesson
        fields = "__all__"
