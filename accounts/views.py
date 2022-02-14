from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string

from .token import account_activation_token

# Create your views here.
# def register(request):
#     if request.method == "POST":
#         #Get form 
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # username = request.POST['username']
        # email = request.POST['email']
        # password = request.POST['password']
        # password2 = request.POST['password2']
        # error = False

        # # Check username
        # if User.objects.filter(username=username):
        #     error = True
        #     messages.error(request, 'Username has been taken')
        # # Check email
        # if User.objects.filter(email=email):
        #     error = True
        #     messages.error(request, 'Email address already in use')
        # # Check if passwords match
        # if password != password2:
        #     error = True
        #     messages.error(request, 'Passwords do not match')
#         if error is False:
#             # Create user
            # user = User.objects.create_user(username=username, email=email, password=password, 
            #                             first_name=first_name, last_name=last_name)
#             #Login after register
#             # auth.login(request, user)
#             # messages.success(request, f'Welcome {user.username}!')
#             # return redirect('pages:index')

#             user.save()
#             messages.success(request, 'You are now registered and can login')
#             return redirect('accounts:login')
#         return redirect('accounts:register')
#     else:
#         return render(request, 'accounts/register.html')

# Register V.2 (Email Verification required)
def register(request):
    if request.method == 'POST':
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

        if error == False:
            user = User.objects.create_user(username=username, email=email, password=password, 
                                        first_name=first_name, last_name=last_name)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please confirm your email address to complete the registration')
            return redirect('pages:index')
        return redirect('accounts:register')
    return render(request, 'accounts/register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        error = False

        user = auth.authenticate(username=username, password=password)

        if user is not None and error is False:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('pages:index')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logged out')
    return redirect('pages:index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('pages:index')
    else:  
        messages.error(request, 'Activation link is invalid!')
        return redirect('pages:index') 