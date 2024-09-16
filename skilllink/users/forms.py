# from typing import Any
# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser, JobSeekerProfile, EmployerProfile
# from django.contrib.auth.forms import AuthenticationForm


# class UserRegistrationForm(UserCreationForm):
#     """
#     used to register the new user based on the CustomUser model
#     it customize usercreationform based on our model
#     """
#     class Meta:
#         """
#         meta class help to specify that the form is intract with the usermodel
#         list the fields to desplay on the form 
#         """
#         model = CustomUser
#         fields = ['email', 'password1', 'password2']

#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         """
#         this constructor will create
#         user all functionality from usercreationform
#         select each fields set a placeholder for the form field
#         """
#         super(UserRegistrationForm, self).__init__(*args, **kwargs)
#         placeholders = {
#             'email': 'Email',
#             'password1': 'Password',
#             'password2': 'Confirm Password',
#             }
#         for field, placeholder in placeholders.items():
#             self.fields[field].widget.attrs['placeholder'] = placeholder
#             self.fields[field].required = True

#         self.fields['password1'].error_messages = {'required': 'Password is required'}
#         self.fields['password2'].error_messages = {'required': 'Please confirm your password'}

#     def clean_email(self):
#         """
#         this method perform custom validation on the email field 
#         first it retrive a email from the form
#         then check the email into the custuser model
#         """
#         email = self.cleaned_data.get('email').lower()
#         if CustomUser.objects.filter(email=email).exists():
#             raise forms.ValidationError(
#                 "A user with this email already exists.")
#         return email
    
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
        
#         if password1 != password2:
#             raise forms.ValidationError("Passwords do not match.")
        
#         if len(password1) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")

#         return password2

# class JobSeekerProfileForm(forms.ModelForm):
#     """
#     FORM FOR JOB SEEKER PROFILE
#     """
#     class Meta:
#         model = JobSeekerProfile
#         fields = ['first_name', 'last_name', 'profile_picture', 'skills', 'experience', 'phone_number']

#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super(JobSeekerProfileForm, self).__init__(*args, **kwargs)
#         placeholders = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'skills': 'Skills',
#             'experience': 'Experience',
#             'phone_number': 'Phone Number'
#         }
#         for field, placeholder in placeholders.items():
#             self.fields[field].widget.attrs['placeholder'] = placeholder
#             self.fields[field].required = True


# class EmployerProfileForm(forms.ModelForm):
#     """
#     FORM FOR JOB EMPLOYER PROFILE
#     """

#     class Meta:
#         model = EmployerProfile
#         fields = ['first_name', 'last_name', 'phone_number', 'location']
    
#     def __init__(self, *args: Any, **kwargs: Any) -> None:
#         super(EmployerProfileForm, self).__init__(*args, **kwargs)
#         placeholders = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'phone_number': 'Phone Number',
#             'location': 'Location'
#         }
#         for field, placeholder in placeholders.items():
#             self.fields[field].widget.attrs['placeholder'] = placeholder
#             self.fields[field].required = True


# class LoginForm(AuthenticationForm):
#     """
#     Form used for login
#     """
#     class Meta:
# #         model = CustomUser
#         fields = ['username', 'password']

#         def __init__(self, *args, **kwargs):
#             super(LoginForm, self).__init__(*args, **kwargs)
#             placeholders = {
#                 'username': 'Email',
#                 'password': 'Password',
#             }
#             for field, placeholder in placeholders.items():
#                 self.fields[field].widget.attrs['placeholder'] = placeholder
#                 self.fields[field].required = True
