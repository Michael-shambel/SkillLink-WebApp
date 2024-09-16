from django import forms
from .models import JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'job_type', 'location', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4})
        }
        