from django.db import models
from users.models import CustomUser
from django.utils import timezone

class JobPost(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.CharField(max_length=255)
    experience_required = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    posted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='job_posts',
        limit_choices_to={'is_employer': True}
    )
    posted_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-posted_on']

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job_post', 'applicant')
    
    def __str__(self):
        return f"{self.applicant.email} - {self.job_post.title}"
