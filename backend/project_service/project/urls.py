from rest_framework.routers import DefaultRouter
from .views import ProjectCategoryViewSet, ProjectViewSet, ProjectTechnologyViewSet

router = DefaultRouter()
router.register(r'project-categories', ProjectCategoryViewSet, basename='project-category')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-technologies', ProjectTechnologyViewSet, basename='project-technology')

urlpatterns = router.urls
