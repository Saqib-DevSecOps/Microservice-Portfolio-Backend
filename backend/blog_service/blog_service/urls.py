from django.urls import path, include, re_path
# EXTERNAL APPS URLS
urlpatterns = [
    path('', include('blog.urls')),  # Include your blog API routes
]


