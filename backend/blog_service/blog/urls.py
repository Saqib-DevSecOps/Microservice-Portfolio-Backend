from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, BlogCategoryViewSet, BlogViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'categories', BlogCategoryViewSet)
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
