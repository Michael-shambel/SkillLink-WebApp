from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from .models import JobPost
from rest_framework.response import Response
from .serializers import JobPostSerializer
from django_filters.rest_framework import DjangoFilterBackend

class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['skills_required', 'location']
    search_fields = ['title', 'description', 'skills_required']

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
