from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from .models import JobPost
from rest_framework.response import Response
from .models import JobPost, Application
from .serializers import JobPostSerializer, JobPostDetailSerializer, ApplicationSerializer, ApplicationCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['skills_required', 'location']
    search_fields = ['title', 'description', 'skills_required']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobPostDetailSerializer
        return JobPostSerializer

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        job_post = self.get_object()
        if not request.user.is_jobseeker:
            return Response({"error": "Only job seekers can apply for jobs"}, status=status.HTTP_403_FORBIDDEN)

        if Application.objects.filter(job_post=job_post, applicant=request.user).exists():
            return Response({"error": "You have already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)

        application = Application.objects.create(job_post=job_post, applicant=request.user)
        return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            return Application.objects.filter(job_post__posted_by=user)
        elif user.is_jobseeker:
            return Application.objects.filter(applicant=user)
        return Application.objects.none()

    def update(self, request, *args, **kwargs):
        if not request.user.is_employer:
            return Response({"error": "Only employers can update application status"}, status=status.HTTP_403_FORBIDDEN)

        application = self.get_object()
        if application.job_post.posted_by != request.user:
            return Response({"error": "You can only update applications for your own job posts"}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
