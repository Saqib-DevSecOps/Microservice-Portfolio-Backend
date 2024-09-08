from rest_framework import viewsets

from .models import Blog, BlogCategory, Tag
from .permission import VerifyUserPermission
from .serializers import BlogSerializer, BlogCategorySerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [VerifyUserPermission]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [VerifyUserPermission]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [VerifyUserPermission]

    def create(self, request, *args, **kwargs):
        # Attach the author ID to the request data from user info
        request.data['author_id'] = request.user_info.get('id')
        return super().create(request, *args, **kwargs)