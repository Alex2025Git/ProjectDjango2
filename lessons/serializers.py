from rest_framework import serializers

from lessons.models import Lesson, Subscription
from lessons.validators import YoutubeValidators


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор по урокам"""

    validators = [YoutubeValidators(field="link_video")]

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ["user_subscription", "course_subscription", "is_subscribed"]

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        course = obj.course_subscription
        return Subscription.objects.filter(
            user_subscription=user, course_subscription=course
        ).exists()
