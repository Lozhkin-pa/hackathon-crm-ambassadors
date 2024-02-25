from rest_framework import viewsets

from ambassadors.models import Course
from api.v1.serializers.course_serializer import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
