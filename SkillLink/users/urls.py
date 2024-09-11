from django.urls import path
from .views import register, select_by_user, job_seeker_profile, employer_profile, login

urlpatterns = [
    path('select-user-type/', select_by_user, name='select_by_user'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('job-seeker-profile/', job_seeker_profile, name='job_seeker_profile'),
    path('employer-profile/', employer_profile, name='employer_profile'),
]
