from rest_framework import viewsets
from .models import Certificate, CertificateCategory
from .serializers import CertificateSerializer, CertificateCategorySerializer


class CertificateCategoryViewSet(viewsets.ModelViewSet):
    queryset = CertificateCategory.objects.all()
    serializer_class = CertificateCategorySerializer


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
