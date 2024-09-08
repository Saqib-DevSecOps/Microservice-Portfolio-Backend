from rest_framework.routers import DefaultRouter
from .views import CertificateViewSet, CertificateCategoryViewSet

router = DefaultRouter()
router.register(r'certificates', CertificateViewSet)
router.register(r'certificate-categories', CertificateCategoryViewSet)

urlpatterns = router.urls
