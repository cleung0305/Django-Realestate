from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        #Get form 
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        error = False

        # Check username
        if User.objects.filter(username=username):
            error = True
            messages.error(request, 'Username has been taken')
        # Check email
        if User.objects.filter(email=email):
            error = True
            messages.error(request, 'Email address already in use')
        # Check if passwords match
        if password != password2:
            error = True
            messages.error(request, 'Passwords do not match')
        if error is False:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password, 
                                        first_name=first_name, last_name=last_name)
            #Login after register
            # auth.login(request, user)
            # messages.success(request, f'Welcome {user.username}!')
            # return redirect('pages:index')

            user.save()
            messages.success(request, 'You are now registered and can login')
            return redirect('accounts:login')
        return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        error = False

        user = auth.authenticate(username=username, password=password)

        if user is not None and error is False:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('pages:index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    return redirect('pages:index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')