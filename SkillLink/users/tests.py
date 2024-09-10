from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import JobSeekerProfile, EmployerProfile
from .forms import UserRegistrationForm, JobSeekerProfileForm, EmployerProfileForm
from .models import CustomUser
from django.urls import reverse, resolve
from .views import register, select_by_user, job_seeker_profile, employer_profile

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='password123',
            is_jobseeker=True
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertTrue(self.user.is_jobseeker)
    
    def test_jobseeker_profile_creation(self):
        profile = JobSeekerProfile.objects.create(user=self.user, first_name='Mike', last_name='sham', phone_number='0974250852', skills='gardner', experience='5 years')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.first_name, 'Mike')
        self.assertEqual(profile.last_name, 'sham')
        self.assertEqual(profile.phone_number, '0974250852')
        self.assertEqual(profile.skills, 'gardner')
        self.assertEqual(profile.experience, '5 years')
    
    def test_employer_profile_creation(self):
        employer_user = get_user_model().objects.create_user(
            email='employer@example.com',
            password='password123',
            is_employer=True
        )
        profile = EmployerProfile.objects.create(user=employer_user, first_name='kerem', last_name='darwash', phone_number='0987654321')
        self.assertEqual(profile.user, employer_user)
        self.assertEqual(profile.first_name, 'kerem')
        self.assertEqual(profile.last_name, 'darwash')
        self.assertEqual(profile.phone_number, '0987654321')

class FormTests(TestCase):

    def test_user_registration_form_valid(self):
        form_data = {
            'email': 'testuser@examole.com',
            'password1': 'password123zxzzx',
            'password2': 'password123zxzzx',
        }
        form = UserRegistrationForm(data=form_data)
        print(form.errors)
        self.assertTrue(form.is_valid(), True)
    
    def test_user_registration_form_invalid_email(self):
        form_data = {
            'email': 'invalid-email',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
    
    def test_jobseeker_profile_form_valid(self):
        form_data = {
            'first_name': 'miki',
            'last_name': 'sham',
            'phone_number': '0987654321',
            'skills': 'Plumber',
            'experience': '5 years',
        }
        form = JobSeekerProfileForm(data=form_data)
        print(form.errors)
        self.assertEqual(form.is_valid(), True)
    
    def test_jobseeker_profile_form_missing_first_name(self):
        form_data = {
            'last_name': 'sham',
            'phone_number': '0987654321',
            'skills': 'plumber',
            'experience': '5 years'
        }
        form = JobSeekerProfileForm(data=form_data)
        self.assertFalse(form.is_valid(), False)
        self.assertIn('first_name', form.errors)
    
    def test_employer_profile_form_valid(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'smith',
            'phone_number': '0987654321',
            'location': 'New York'
        }
        form = EmployerProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_employer_profile_form_missing_phone_number(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'location': 'New York',
        }
        form = EmployerProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class UrlTests(TestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)
    
    def test_select_user_type_url_resolves(self):
        url = reverse('select_by_user')
        self.assertEqual(resolve(url).func, select_by_user)
    
    def test_job_seeker_profile_url_resolves(self):
        url = reverse('job_seeker_profile')
        self.assertEqual(resolve(url).func, job_seeker_profile)
    
    def test_employer_profile_url_resolves(self):
        url = reverse('employer_profile')
        self.assertEqual(resolve(url).func, employer_profile)