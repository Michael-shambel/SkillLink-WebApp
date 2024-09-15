from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'job-posts', views.JobPostViewSet, basename='job-post')

urlpatterns = [
    path('api/', include(router.urls)),
]