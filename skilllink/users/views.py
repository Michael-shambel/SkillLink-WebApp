from rest_framework import viewsets, status, filters
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer, TokenSerializer, JobSeekerReviewSerializer, JobSeekerProfileDetailSerializer
from .models import JobSeekerProfile, EmployerProfile, JobSeekerReview
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        is_employer = request.data.get('is_employer', False)
        is_jobseeker = request.data.get('is_jobseeker', False)
    
        if not email or not password:
            return Response({'error': 'Email and Password Required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            email=email,
            password=password,
            is_employer=is_employer,
            is_jobseeker=is_jobseeker
        )
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({
            'message': 'User created successfully',
            'user': serializer.data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    

class TokenViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            serializer = TokenSerializer(token)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_jobseeker:
            return JobSeekerProfile.objects.filter(user=user)
        return JobSeekerProfile.objects.none()
    
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     if not user.is_jobseeker:
    #         raise PermissionDenied('Only job seekers can create a profile')
    #     serializer.save(user=user)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_jobseeker:
            return Response({'error': 'Only job seekers can create a profile'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobSeekerProfileDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        job_seeker = self.get_object()
        employer = request.user

        if not employer.is_employer:
            return Response({"error": "Only employers can leave reviews"}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSeekerReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer, job_seeker=job_seeker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            return EmployerProfile.objects.filter(user=user)
        return EmployerProfile.objects.none()
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_employer:
            return Response({'error': 'Only employers can create a profile'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class JobSeekerSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['skills']

    def get_queryset(self):
        if self.request.user.is_employer:
            return JobSeekerProfile.objects.all()
        return JobSeekerProfile.objects.none()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return JobSeekerProfileDetailSerializer
        return self.serializer_class
