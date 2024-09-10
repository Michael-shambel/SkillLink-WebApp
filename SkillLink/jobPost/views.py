from django.shortcuts import render
from .models import JobPost
from django.db.models import Q

def job_list(request):
    job_posts = JobPost.objects.all()
    return render(request, 'jobPost/job_list.html', {'job_posts': job_posts})

def job_search(request):
    query = request.GET.get('q')
    job_posts = JobPost.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(skills_required__icontains=query)
    )
    return render(request, 'jobPost/job_list.html', {'job_posts': job_posts})
