from django.urls import path
from . import views as user_views # register, select_by_user, job_seeker_profile, employer_profile, login, home

urlpatterns = [
    path('', user_views.home, name='main-home'),
    path('select-user-type/', user_views.select_by_user, name='select_by_user'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('job-seeker-profile/', user_views.job_seeker_profile, name='job_seeker_profile'),
    path('employer-profile/', user_views.employer_profile, name='employer_profile'),
]
