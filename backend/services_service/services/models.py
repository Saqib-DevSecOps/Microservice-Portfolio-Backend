from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the technology
    thumbnail_image = models.ImageField(upload_to='technology_thumbnails/', blank=True, null=True)  # Thumbnail image
    description = models.TextField(blank=True, null=True)  # Optional description of the technology
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return self.name


class Skill(models.Model):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4
    MASTER = 5

    PROFICIENCY_LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
        (MASTER, 'Master'),
    ]

    name = models.CharField(max_length=100, unique=True)  # Name of the skill
    description = models.TextField(blank=True, null=True)  # Optional description of the skill
    proficiency_level = models.IntegerField(
        choices=PROFICIENCY_LEVEL_CHOICES,
        default=BEGINNER
    )  # Skill level with choices from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the service category
    description = models.TextField(blank=True, null=True)  # Optional description of the service category
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=200)  # Title of the service
    description = models.TextField()  # Detailed description of the service
    category = models.ForeignKey(ServiceCategory, related_name='services',
                                 on_delete=models.CASCADE)  # Link to ServiceCategory
    thumbnail_image = models.ImageField(upload_to='service_thumbnails/', blank=True, null=True)  # Thumbnail image
    is_active = models.BooleanField(default=True)  # Whether the service is active
    skills = models.ManyToManyField(Skill, related_name='services', blank=True)  # Skills required for the service
    technologies = models.ManyToManyField(Technology, related_name='services',
                                          blank=True)  # Technologies used in the service
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return self.title
