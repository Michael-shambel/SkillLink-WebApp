from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    """
    used to register the new user based on the CustomUser model
    it customize usercreationform based on our model
    """
    class Meta:
        """
        meta class help to specify that the form is intract with the usermodel
        list the fields to desplay on the form 
        """
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        this constructor will create
        user all functionality from usercreationform
        select each fields set a placeholder for the form field
        """
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs[
            'placeholder'] = 'Confirm Password'

    def clean_email(self):
        """
        this method perform custom validation on the email field 
        first it retrive a email from the form
        then check the email into the custuser model
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists.")
        return email
