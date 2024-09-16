from rest_framework import serializers
from .models import JobPost, Application
from users.serializers import UserSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'status', 'applied_at', 'updated_at']
        read_only_fields = ['id', 'applicant', 'applied_at', 'updated_at']

class JobPostSerializer(serializers.ModelSerializer):
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = JobPost
        fields = ['id', 'title', 'description', 'skills_required', 'experience_required', 'location', 'posted_by', 'posted_on', 'applications_count']
        read_only_fields = ['posted_by', 'posted_on', 'applications_count']
    
    def get_applications_count(self, obj):
        return obj.applications.count()

class JobPostDetailSerializer(JobPostSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)

    class Meta(JobPostSerializer.Meta):
        fields = JobPostSerializer.Meta.fields + ['applications']

class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['job_post']
