from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer, TokenSerializer
from .models import JobSeekerProfile, EmployerProfile

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

# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from .serializers import UserSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer, TokenSerializer
# from .models import JobSeekerProfile, EmployerProfile

# User = get_user_model()

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     is_employer = request.data.get('is_employer', False)
#     is_jobseeker = request.data.get('is_jobseeker', False)

#     if not email or not password:
#         return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#     if User.objects.filter(email=email).exists():
#         return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

#     user = User.objects.create(
#         email=email,
#         password=make_password(password),
#         is_employer=is_employer,
#         is_jobseeker=is_jobseeker
#     )
#     Token.objects.create(user=user)
#     return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def obtain_token(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     user = User.objects.filter(email=email).first()
#     if user and user.check_password(password):
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def list_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_job_seeker_profile(request):
#     user = request.user
#     if not user.is_jobseeker:
#         return Response({'error': 'Only job seekers can create a profile'}, status=status.HTTP_403_FORBIDDEN)

#     serializer = JobSeekerProfileSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_employer_profile(request):
#     user = request.user
#     if not user.is_employer:
#         return Response({'error': 'Only employers can create a profile'}, status=status.HTTP_403_FORBIDDEN)

#     serializer = EmployerProfileSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_job_seeker_profile(request):
#     user = request.user
#     try:
#         profile = user.jobseeker_profile
#     except JobSeekerProfile.DoesNotExist:
#         return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = JobSeekerProfileSerializer(profile, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_employer_profile(request):
#     user = request.user
#     try:
#         profile = user.employer_profile
#     except EmployerProfile.DoesNotExist:
#         return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
