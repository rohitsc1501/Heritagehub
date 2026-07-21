from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_notifications, name='list-notifications'),
    path('<int:pk>/read/', views.mark_read, name='mark-read'),
    path('read-all/', views.mark_all_read, name='mark-all-read'),
]
