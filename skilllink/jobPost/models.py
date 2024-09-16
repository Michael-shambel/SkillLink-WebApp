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
