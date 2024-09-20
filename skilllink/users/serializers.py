from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import JobSeekerProfile, EmployerProfile, JobSeekerReview

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_employer', 'is_jobseeker']

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'profile_picture', 'skills', 'experience', 'phone_number']
        read_only_fields = ['id', 'user']
    
    def validate_profile_picture(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image file too large ( > 5MB )")
            return value

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'location', 'phone_number']
        read_only_fields = ['id', 'user']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class JobSeekerReviewSerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = JobSeekerReview
        fields = ['id', 'employer', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'employer', 'created_at']

class JobSeekerProfileDetailSerializer(JobSeekerProfileSerializer):
    reviews = JobSeekerReviewSerializer(many=True, read_only=True, source='reviews_received')
    average_rating = serializers.SerializerMethodField()

    class Meta(JobSeekerProfileSerializer.Meta):
        fields = JobSeekerProfileSerializer.Meta.fields + ['reviews', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews_received.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None
