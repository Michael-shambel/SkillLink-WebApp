from django.urls import path
from . import views

urlpatterns = [
    path('job-posts/', views.job_post_list, name='job_post_list'),
    path('job-post/create/', views.job_post_create, name='job_post_create'),
    path('job-post/<int:pk>/update/', views.job_post_update, name='job_post_update'),
    path('job-post/<int:pk>/delete/', views.job_post_delete, name='job_post_delete'),
]
