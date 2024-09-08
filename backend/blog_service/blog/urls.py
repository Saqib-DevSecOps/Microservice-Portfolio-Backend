from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, BlogViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'blog-categories', CategoryViewSet)
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
