from django.db import models


class CertificateCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Certificate(models.Model):
    title = models.CharField(max_length=255)  # Name of the certificate
    category = models.ForeignKey('CertificateCategory', related_name='certificates', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    issuer = models.CharField(max_length=255)  # Organization that issued the certificate
    issue_date = models.DateField()  # Date when the certificate was issued
    expiration_date = models.DateField(blank=True, null=True)  # If the certificate expires
    certificate_url = models.URLField(max_length=500, blank=True, null=True)  # URL to view/download the certificate
    verification_url = models.URLField(max_length=500, blank=True,
                                       null=True)  # URL to verify the certificate's authenticity
    certificate_id = models.CharField(max_length=100, unique=True, blank=True,
                                      null=True)  # Unique ID for the certificate
    grade = models.CharField(max_length=100, blank=True, null=True)  # Grade or score received (if applicable)
    description = models.TextField(blank=True, null=True)  # Additional details about the certificate
    logo = models.ImageField(upload_to='certificates/logos/', blank=True,
                             null=True)  # Logo or image of the certificate or issuer
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the certificate is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set when the certificate is updated

    def __str__(self):
        return f"{self.title} by {self.issuer}"

    class Meta:
        ordering = ['issue_date']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
