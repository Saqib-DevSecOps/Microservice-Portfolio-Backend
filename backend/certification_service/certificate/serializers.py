from rest_framework import serializers
from .models import Certificate, CertificateCategory

class CertificateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class CertificateSerializer(serializers.ModelSerializer):
    category = CertificateCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=CertificateCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Certificate
        fields = [
            'id', 'title', 'category', 'category_id', 'issuer', 'issue_date', 'expiration_date',
            'certificate_url', 'verification_url', 'certificate_id', 'grade', 'description',
            'logo', 'created_at', 'updated_at'
        ]
