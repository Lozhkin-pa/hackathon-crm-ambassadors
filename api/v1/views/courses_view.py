from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from ambassadors.models import Course
from api.v1.serializers.course_serializer import CourseSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("title", "id")
