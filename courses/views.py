from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseDetailSerializer, CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer
