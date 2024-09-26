from rest_framework import viewsets, status, filters
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, JobSeekerProfileSerializer, EmployerProfileSerializer, TokenSerializer, JobSeekerReviewSerializer, JobSeekerProfileDetailSerializer
from .models import JobSeekerProfile, EmployerProfile, JobSeekerReview
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
import os
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CLIENT_ID = os.getenv('VUE_APP_GOOGLE_CLIENT_ID');
User = get_user_model()

class UserViewSet(viewsets.ViewSet):
    """
    User viewsets for authentication and registration.
    anyone allowed to create a user.
    and we define only create method here for registration.
    we use TokenAuthentication for authentication.
    """
    permission_classes = [AllowAny]

    def create(self, request):
        """
        create a new user.
        email, password, is_employer, is_jobseeker are retrived from the request.
        if email or password is not provided, we return an error.
        if the provided email is already in use, we return an error.
        if not it creates a new user.
        then we create a token for the user.
        then we serialie the user object and return the response.

        """
        email = request.data.get('email')
        password = request.data.get('password')
        is_employer = request.data.get('is_employer', False)
        is_jobseeker = request.data.get('is_jobseeker', False)

        if not email or not password:
            return Response({'error': 'Email and Password Required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_409_CONFLICT)

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

        @api_view(['POST'])
        def google_register(self, request):
            """A user who chooses to sign up using Google doesn't manually enter their
               email and password. Instead, they authenticate with Google, which provides an
               ID token that verifies the user's identity.
               Backend then uses this ID token to either register the user (if they don't exist) or
               log them in (if they already exist
            """
            token = request.data.get('google_token')

            try:
                idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), 'GOOGLE_CLIENT_ID')
                email = idinfo['email']

                if User.objects.filter(email=email).exists():
                    return Response({'error': 'User already exists'}, status=status.HTTP_409_CONFLICT)

                is_employer = request.data.get('is_employer', False)
                is_jobseeker = not is_employer

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    is_employer=is_employer,
                    is_jobseeker=is_jobseeker
                )

                user.set_unusable_password()
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                serializer = UserSerializer(user)
                return Response({
                    'success': True,
                    'user': serializer.data,
                    'token': token.key
                }, status=status.HTTP_201_CREATED)

            except ValueError:
                return Response({"success": False, "error": "Invalid token"}, status=400)


class TokenViewSet(viewsets.ViewSet):
    """
    Token viewsets for authentication.
    anyone allowed to create a token.
    we define only create method here for token creation.
    we use TokenAuthentication for authentication.
    we check if the email and password are correct.
    if correct we create a token for the user.
    then we serialie the token object and return the response.
    """
    permission_classes = [AllowAny]

    def create(self, request):
        """
        email and password are retrived from the request.
        we check if the email and password are correct.
        if correct we create a token for the user.
        then we serialie the token object and return the response.
        """
        google_token = request.data.get('google_token')
        if google_token:
            return self.handle_google_login(google_token) # Check if it's a Google login request

        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            serializer = TokenSerializer(token)
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'is_employer': user.is_employer,
                    'is_jobseeker': user.is_jobseeker,
                }
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    def handle_google_login(self, google_token):
        """GOOGLE AUTHENTICATION
           ---------------------
        - Once the user has registered with Google (or if they already have an account), they can use Google to log in
        - Django will generate tokens on the backend and sent to frontend where they are stored in localstorage
        - The google_token contains a payload that has users details.
        - If token is valid, you fetch or create the user and generate a Django token for that user.
        """
        try:
            # Verify the Google token with Google's API
            idinfo = id_token.verify_oauth2_token(google_token, google_requests.Request(), GOOGLE_CLIENT_ID)

            email = idinfo.get('email')
            name = idinfo.get('name')
            google_user_id = idinfo.get('sub')

            # Check if user exists, or create a new user
            user, created = User.objects.get_or_create(email=email, defaults={'username': email})

            # Create or get a Django token for the user
            token, _ = Token.objects.get_or_create(user=user)

            # Return token and user info
            return Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'is_employer': user.is_employer,
                    'is_jobseeker': user.is_jobseeker,
                }
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)


class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    """
    Job seeker profile viewsets for the job seeker profile model.
    we use IsAuthenticated permission for the job seeker profile viewsets.
    we define only create, update, destroy, retrieve, list methods here.
    we use JobSeekerProfileSerializer for the job seeker profile serializer.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    def get_queryset(self):
        """
        get the job seeker profile object for the current user.
        """
        user = self.request.user
        if user.is_jobseeker:
            return JobSeekerProfile.objects.filter(user=user)
        return JobSeekerProfile.objects.none()

    def update(self, request, *args, **kwargs):
        """
        update the job seeker profile object for the current user.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_object(self):
        """
        get the job seeker profile object for the current user.
        """
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is None:
            raise Http404("JobSeekerProfile not found")
        return obj

    def create(self, request, *args, **kwargs):
        """
        create a new job seeker profile object for the current user.
        """
        user = request.user
        if not user.is_jobseeker:
            return Response({'error': 'Only job seekers can create a profile'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        """
        get the serializer class for the job seeker profile.
        """
        if self.action == 'retrieve':
            return JobSeekerProfileDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def review(self, request, pk=None):
        """
        create a new job seeker review object for the current user.
        """
        try:
            job_seeker = JobSeekerProfile.objects.get(pk=pk)
        except JobSeekerProfile.DoesNotExist:
            raise Http404("JobSeekerProfile not found")

        employer = request.user

        if not employer.is_employer:
            return Response({"error": "Only employers can leave reviews"}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobSeekerReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer, job_seeker=job_seeker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """
        destroy the job seeker profile object for the current user.
        """
        instance = self.get_object()
        if  instance.user != request.user:
            raise PermissionDenied("You don't have permission to delete this profile.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployerProfileViewSet(viewsets.ModelViewSet):
    """
    Employer profile viewsets for the employer profile model.
    we use IsAuthenticated permission for the employer profile viewsets.
    we define only create, update, destroy, retrieve, list methods here.
    we use EmployerProfileSerializer for the employer profile serializer.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerProfileSerializer

    def get_queryset(self):
        """
        get the employer profile object for the current user.
        """
        user = self.request.user
        if user.is_employer:
            return EmployerProfile.objects.filter(user=user)
        return EmployerProfile.objects.none()

    def create(self, request, *args, **kwargs):
        """
        create a new employer profile object for the current user.
        """
        user = request.user
        if not user.is_employer:
            return Response({'error': 'Only employers can create a profile'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        update the employer profile object for the current user.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        destroy the employer profile object for the current user.
        """
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You don't have permission to delete this profile.")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        """
        get the employer profile object for the current user.
        """
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is None:
            raise Http404("EmployerProfile not found")
        return obj


class JobSeekerSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Job seeker search viewsets for the job seeker profile model.
    we use IsAuthenticated permission for the job seeker search viewsets.
    we define only retrieve, list methods here.
    we use JobSeekerProfileSerializer for the job seeker profile serializer.
    """
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['skills']

    def get_queryset(self):
        """
        get the job seeker profile object for the current user.
        """
        if self.request.user.is_employer:
            return JobSeekerProfile.objects.all()
        return JobSeekerProfile.objects.none()

    def get_serializer_class(self):
        """
        get the serializer class for the job seeker profile.
        """
        if self.action == 'retrieve':
            return JobSeekerProfileDetailSerializer
        return self.serializer_class
