from django.db import models

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique name for the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)  # Title of the project
    description = models.TextField()  # Detailed description of the project
    thumbnail_image = models.ImageField(upload_to='project_thumbnails/', blank=True, null=True)  # Thumbnail image for the project
    category = models.ForeignKey(ProjectCategory, related_name='projects', on_delete=models.CASCADE)  # Link to ProjectCategory
    start_date = models.DateField()  # Start date of the project
    end_date = models.DateField(blank=True, null=True)  # Optional end date of the project
    is_active = models.BooleanField(default=True)  # Status of the project (active or not)
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update
    def __str__(self):
        return self.title


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, related_name='technologies', on_delete=models.CASCADE)  # Link to Project
    technology_id = models.IntegerField()  # ID of the technology used in the project
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update

    def __str__(self):
        return f"{self.project.title} - {self.technology_id}"

