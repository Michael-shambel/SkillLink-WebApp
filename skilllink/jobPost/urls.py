"""This router handles the standard CRUD operations for job posts and applications
   The custom api/job-posts/<int:job_post_id>/applicants/ is added to fetch the list
   of applicants for a specific job post by passing their jop_pos_id.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'job-posts', views.JobPostViewSet, basename='job-post')
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    path('api/', include(router.urls)),
    # Custom URL for fetching applicants for a specific job post
    path('api/job-posts/<int:job_post_id>/applicants/', views.JobApplicantsViewSet.as_view({'get': 'list'}), name='job-applicants'),
]
