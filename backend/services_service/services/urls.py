from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TechnologyViewSet, SkillViewSet, ServiceCategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'technologies', TechnologyViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'service-categories', ServiceCategoryViewSet)
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
