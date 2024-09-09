from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, JobSeekerProfileForm, EmployerProfileForm
from .models import JobSeekerProfile, EmployerProfile



def select_by_user(request):
    """
    this view presents a page where the user select user type
    either "employer" or "job seeker"
    the user type is stored in session which is buitin django
    and we later user it in registration process
    first
        the user_type will retrive from the data 
        stored in session and redirect to the registration
    """
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.session['user_type'] = user_type
        return redirect('register')

    return render(request, 'users/select_user_type.html')


def register(request):
    """
    this method will handle the user registration process.
    first it will chack the user_type is in session if not it will redirect
    to the select_by_user page if user_type is in sessions
    if the request is POST create an instance of UserRegistrationForm witht the data
    check if the form is valid by using form.is_valid()
    save the email and password and user_type into DB
    """
    if 'user_type' not in request.session:
        return redirect('select_by_user')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user_type = request.session['user_type']
            user.email = form.cleaned_data.get('email')
            user.set_password(form.cleaned_data['password1'])
            if user_type == 'employer':
                user.is_employer = True
            elif user_type == 'job_seeker':
                user.is_jobseeker = True

            user.save()
            del request.session['user_type'] 
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def job_seeker_profile(request):
    user = request.user
    profile, created = JobSeekerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('job_seeker_profile')
        else:
            form = JobSeekerProfileForm(instance=profile)
    return render(request, 'users/job_seeker_profile.html', {'form': form})

@login_required
def employer_profile(request):
    user = request.user
    profile, created = EmployerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=profile)
    return render(request, 'users/employer_profile.html', {'form': form})
