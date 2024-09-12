from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from .models import JobPost


@login_required
def job_post_list(request):
    job_posts = JobPost.objects.filter(employer=request.user)
    return render(request, 'jobs/job_post_list.html', {'job_posts': job_posts})

@login_required
def job_post_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.employer = request.user
            job_post.save()
            return redirect('job_post_list')
    else:
        form = JobPostForm()
    return render(request, 'jobs/job_post_form.html', {'form': form})

@login_required
def job_post_update(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job_post)
        if form.is_valid():
            form.save()
            return redirect('job_post_list')
    else:
        form = JobPostForm(instance=job_post)
    return render(request, 'jobs/job_post_form.html', {'form': form})

@login_required
def job_post_delete(request, pk):
    job_post = get_object_or_404(JobPost, pk=pk, employer=request.user)
    if request.method == 'POST':
        job_post.delete()
        return redirect('job_post_list')
    return render(request, 'jobs/job_post_confirm_delete.html', {'job_post': job_post})