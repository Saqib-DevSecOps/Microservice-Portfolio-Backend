from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.database import engine
from app.models.projects import ProjectCategory, Project
from app.models.services import ServiceCategory, Service
from app.models.users import User

app = FastAPI()

admin = Admin(app, engine)
class UserAdmin(ModelView, model=User):
    column_list = [User.id,]


class ServiceCategoryAdmin(ModelView, model=ServiceCategory):
    column_list = [ServiceCategory.id, ServiceCategory.name, ServiceCategory.description]

class ServiceAdmin(ModelView, model=Service):
    column_list = [Service.id, Service.name, Service.description, Service.category_id]

class ProjectCategoryAdmin(ModelView, model=ProjectCategory):
    column_list = [ProjectCategory.id, ProjectCategory.name, ProjectCategory.description]

class ProjectAdmin(ModelView, model=Project):
    column_list = [Project.id, Project.name, Project.description,  Project.project_url, Project.category_id]

admin.add_view(UserAdmin)
admin.add_view(ServiceCategoryAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(ProjectCategoryAdmin)
admin.add_view(ProjectAdmin)