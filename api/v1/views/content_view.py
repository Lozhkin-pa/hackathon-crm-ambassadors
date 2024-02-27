from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import decorators, permissions, status, viewsets
from rest_framework.response import Response

from ambassadors.models import Ambassador
from api.v1.filters import ContentFilter
from api.v1.serializers.content_serializer import (
    CreateContentSerializer,
    FormsContentSerializer,
    ListContentSerializer,
    RetrieveContentSerializer,
)
from content.models import Content


class ContentViewSet(viewsets.ModelViewSet):
    """Контент амбассадора."""
    
    queryset = Content.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ContentFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ListContentSerializer
        if self.action == 'retrieve':
            return RetrieveContentSerializer
        if self.action in ['create', 'partial_update']:
            return CreateContentSerializer

    @decorators.action(
        methods=('post',),
        detail=False,
        url_name='forms', # Полный url: .../api/v1/content/forms/
        permission_classes=(permissions.AllowAny,)
    )
    def get_content_from_forms(self, request):
        """Получение контента амбассадора из Яндекс Формы."""

        if Ambassador.objects.filter(
            telegram=request.data.get('telegram')
        ).exists():
            serializer = FormsContentSerializer(data=request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
