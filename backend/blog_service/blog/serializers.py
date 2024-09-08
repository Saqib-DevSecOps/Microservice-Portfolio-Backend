from rest_framework import serializers
from .models import Tag, BlogCategory, Blog

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'slug', 'description']

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = BlogCategorySerializer(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'author_id', 'content', 'excerpt', 'cover_image',
            'tags', 'category', 'created_at', 'updated_at', 'status', 'views'
        ]
