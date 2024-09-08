from rest_framework import viewsets
from .models import Tag, BlogCategory, Blog
from .serializers import TagSerializer, BlogCategorySerializer, BlogSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
