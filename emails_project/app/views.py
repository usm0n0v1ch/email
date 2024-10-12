from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from .models import UserProfile
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            token = get_random_string(length=64)
            UserProfile.objects.create(user=user, confirmation_token=token)

            confirmation_url = request.build_absolute_uri(
                reverse('confirm_account', args=[token])
            )
            send_mail(
                'Confirm your account',
                f'Click the link to confirm your account: {confirmation_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return redirect('confirmation_sent')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def confirm_account(request, token):
    user_profile = get_object_or_404(UserProfile, confirmation_token=token)
    if not user_profile.is_confirmed:
        user_profile.is_confirmed = True
        user_profile.user.is_active = True
        user_profile.user.save()
        user_profile.save()

    return render(request, 'account_confirmed.html')

def confirmation_sent(request):
    return render(request, 'confirmation_sent.html')

def account_not_confirmed(request):
    return render(request, 'account_not_confirmed.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.userprofile.is_confirmed:
                    login(request, user)
                    return redirect('home')
                else:
                    return redirect('account_not_confirmed')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid login credentials'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')