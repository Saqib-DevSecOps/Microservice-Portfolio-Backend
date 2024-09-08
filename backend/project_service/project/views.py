from rest_framework import viewsets
from .models import ProjectCategory, Project, ProjectTechnology
from .serializers import ProjectCategorySerializer, ProjectSerializer, ProjectTechnologySerializer
from .permissions import VerifyUserPermission


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    permission_classes = [VerifyUserPermission]



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [VerifyUserPermission]



class ProjectTechnologyViewSet(viewsets.ModelViewSet):
    queryset = ProjectTechnology.objects.all()
    serializer_class = ProjectTechnologySerializer
    permission_classes = [VerifyUserPermission]

