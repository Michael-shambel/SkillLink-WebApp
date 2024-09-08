from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def select_by_user(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        request.session['user_type'] = user_type
        return redirect('register')

    return render(request, 'users/select_user_type.html')

def register(request):
    if 'user_type' not in request.session:
        return redirect('select_by_user')

    if request.method =='POST':
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
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
