from django.urls import path
from .views import (
    register_user, 
    obtain_token, 
    list_users, 
    create_job_seeker_profile, 
    create_employer_profile, 
    update_job_seeker_profile, 
    update_employer_profile
)

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/token/', obtain_token, name='obtain_token'),
    path('api/users/', list_users, name='list_users'),
    
    # Profile management
    path('api/profile/jobseeker/create/', create_job_seeker_profile, name='create_job_seeker_profile'),
    path('api/profile/employer/create/', create_employer_profile, name='create_employer_profile'),
    path('api/profile/jobseeker/update/', update_job_seeker_profile, name='update_job_seeker_profile'),
    path('api/profile/employer/update/', update_employer_profile, name='update_employer_profile'),
]
