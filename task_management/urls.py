from django.urls import path
from . import views
urlpatterns = [
    path('', views.login),
    path('UserLogin/', views.LoginValidate),
    path('UserRegistration/', views.Create_Users),
    path('ProjectList/', views.ProjectList),
    path('ProjectInsertUpdate/', views.ProjectInsertUpdate),
    path('getProjectlist/', views.getProjectlist),
    path('ProjectDelete/', views.ProjectDelete),
    path('ProjectDetails/<slug:ProjectID>/', views.ProjectDetails),
    path('getTasklist/', views.getTasklist),
    path('TaskInsertUpdate/', views.TaskInsertUpdate),
    path('getAssigneeName/', views.getAssigneeName),
    path('TaskDelete/', views.TaskDelete),
    path('ProjectDetails/<slug:ProjectID>/task/<slug:TaskID>/', views.TaskDetails)
]
