from rest_framework import serializers
from .models import ProjectCategory, Project, ProjectTechnology

class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'thumbnail_image', 'category', 'start_date', 'end_date', 'is_active', 'technologies', 'created_at', 'updated_at']

class ProjectTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTechnology
        fields = ['id', 'project', 'technology_id', 'created_at', 'updated_at']
