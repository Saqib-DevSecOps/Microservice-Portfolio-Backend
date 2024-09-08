from rest_framework import viewsets
from .models import Tag, BlogCategory, Blog
from .serializers import TagSerializer, BlogCategorySerializer, BlogSerializer
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
import requests

class TokenVerificationPermission(permissions.BasePermission):
    API_GATEWAY_URL = "http://127.0.0.1:8000/verify-token/"  # Update with your API Gateway URL

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS requests

        token = request.headers.get('Authorization')
        if not token:
            raise PermissionDenied("Authorization header is missing")

        headers = {'Authorization': token}
        response = requests.post(self.API_GATEWAY_URL, headers=headers)

        if response.status_code == 200:
            user_info = response.json().get('user_info')
            if user_info:
                # Attach user info to the request for later use
                request.user_info = user_info
                return True
            else:
                raise PermissionDenied("Invalid token response")
        else:
            raise PermissionDenied("Invalid token")


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [TokenVerificationPermission]

    def create(self, request, *args, **kwargs):
        # Attach the author ID to the request data
        request.data['author_id'] = request.user_info.get('id')
        return super().create(request, *args, **kwargs)
