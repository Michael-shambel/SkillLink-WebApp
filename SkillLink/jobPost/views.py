from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import JobPost
from rest_framework.response import Response
from .serializers import JobPostSerializer

class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_employer:
            return JobPost.objects.filter(posted_by=self.request.user)
        return JobPost.objects.all()
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_employer:
            return Response({"error": "Only employer can create job posts"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(posted_by=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import JobPostForm
# from .models import JobPost


# # @login_required
# def job_post_list(request):
#     job_posts = JobPost.objects.filter(employer=request.user)
#     return render(request, 'jobs/job_post_list.html', {'job_posts': job_posts})

# @login_required
# def job_post_create(request):
#     if request.method == 'POST':
#         form = JobPostForm(request.POST)
#         if form.is_valid():
#             job_post = form.save(commit=False)
#             job_post.employer = request.user
#             job_post.save()
#             return redirect('job_post_list')
#     else:
#         form = JobPostForm()
#     return render(request, 'jobs/job_post_form.html', {'form': form})

# @login_required
# def job_post_update(request, pk):
#     job_post = get_object_or_404(JobPost, pk=pk, employer=request.user)
#     if request.method == 'POST':
#         form = JobPostForm(request.POST, instance=job_post)
#         if form.is_valid():
#             form.save()
#             return redirect('job_post_list')
#     else:
#         form = JobPostForm(instance=job_post)
#     return render(request, 'jobs/job_post_form.html', {'form': form})

# @login_required
# def job_post_delete(request, pk):
#     job_post = get_object_or_404(JobPost, pk=pk, employer=request.user)
#     if request.method == 'POST':
#         job_post.delete()
#         return redirect('job_post_list')
#     return render(request, 'jobs/job_post_confirm_delete.html', {'job_post': job_post})