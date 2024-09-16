from rest_framework import serializers
from .models import JobPost

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'description', 'skills_required', 'experience_required', 'location', 'posted_by', 'posted_on']
        read_only_fields = ['posted_by', 'posted_on']
