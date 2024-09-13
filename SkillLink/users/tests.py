from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import JobSeekerProfile, EmployerProfile

User = get_user_model()

class UserRegistrationTest(APITestCase):
    
    def test_register_user(self):
        """
        Test user registration with valid data
        """
        url = reverse('register_user')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'is_jobseeker': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@example.com')

    def test_register_user_missing_email(self):
        """
        Test user registration with missing email
        """
        url = reverse('register_user')
        data = {
            'password': 'testpassword123',
            'is_jobseeker': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate_email(self):
        """
        Test user registration with duplicate email
        """
        User.objects.create_user(email='testuser@example.com', password='testpassword123')
        url = reverse('register_user')
        data = {
            'email': 'testuser@example.com',
            'password': 'newpassword456',
            'is_jobseeker': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TokenAuthenticationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword123')
    
    def test_obtain_token(self):
        """
        Test token retrieval with valid credentials
        """
        url = reverse('obtain_token')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_obtain_token_invalid_credentials(self):
        """
        Test token retrieval with invalid credentials
        """
        url = reverse('obtain_token')
        data = {
            'email': 'wronguser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class JobSeekerProfileTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='jobseeker@example.com', password='testpassword123', is_jobseeker=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_job_seeker_profile(self):
        """
        Test creating a job seeker profile
        """
        url = reverse('create_job_seeker_profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'skills': 'Python, Django',
            'experience': '5 years of experience',
            'phone_number': '123456789'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobSeekerProfile.objects.count(), 1)
        self.assertEqual(JobSeekerProfile.objects.get().first_name, 'John')

    def test_update_job_seeker_profile(self):
        """
        Test updating a job seeker profile
        """
        profile = JobSeekerProfile.objects.create(user=self.user, first_name='John', last_name='Doe', skills='Python')
        url = reverse('update_job_seeker_profile')
        data = {
            'skills': 'Python, Django, React'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.skills, 'Python, Django, React')

class EmployerProfileTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='employer@example.com', password='testpassword123', is_employer=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_employer_profile(self):
        """
        Test creating an employer profile
        """
        url = reverse('create_employer_profile')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'location': 'New York',
            'phone_number': '987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployerProfile.objects.count(), 1)
        self.assertEqual(EmployerProfile.objects.get().first_name, 'Jane')

    def test_update_employer_profile(self):
        """
        Test updating an employer profile
        """
        profile = EmployerProfile.objects.create(user=self.user, first_name='Jane', last_name='Doe')
        url = reverse('update_employer_profile')
        data = {
            'location': 'San Francisco'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profile.refresh_from_db()
        self.assertEqual(profile.location, 'San Francisco')
