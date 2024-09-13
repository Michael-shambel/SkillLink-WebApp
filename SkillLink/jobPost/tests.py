from django.test import TestCase
from django.utils import timezone
from users.models import CustomUser
from .models import JobPost


class JobPostModelTest(TestCase):
    def setUp(self):
        self.employer = CustomUser.objects.create_user(
            email='testcase@company.com',
            password='password',
            is_employer=True
        )
    
    def test_job_post_creation(self):
        job_post = JobPost.objects.create(
            title='gardener',
            description='a person who can take care of the garden',
            skills_required='gardening',
            experience_required='2 years',
            location='Bangalore',
            posted_by=self.employer,
            posted_on=timezone.now()
        )
        self.assertEqual(job_post.title, 'gardener')
        self.assertEqual(job_post.description, 'a person who can take care of the garden')
        self.assertEqual(job_post.skills_required, 'gardening')
        self.assertEqual(job_post.experience_required, '2 years')
        self.assertEqual(job_post.location, 'Bangalore')
        self.assertEqual(job_post.posted_by, self.employer)
        self.assertIsNotNone(job_post.posted_on)
