from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TokenViewSet, JobSeekerProfileViewSet, EmployerProfileViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register the UserViewSet and TokenViewSet (for authentication)
router.register(r'register', UserViewSet, basename='register')
router.register(r'token', TokenViewSet, basename='token')

# Register the JobSeekerProfileViewSet and EmployerProfileViewSet (for profiles)
router.register(r'jobseekers', JobSeekerProfileViewSet, basename='jobseeker')
router.register(r'employers', EmployerProfileViewSet, basename='employer')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]
