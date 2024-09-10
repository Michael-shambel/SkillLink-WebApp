from django.urls import path
from .views import job_list, job_search

urlpatterns = [
    path('jobs/', job_list, name='job_list'),
    path('jobs/search/', job_search, name='job_search')
]
