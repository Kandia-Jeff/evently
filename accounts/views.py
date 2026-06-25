from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, VerificationForm
from django.contrib.auth.forms import AuthenticationForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, f'Welcome to Evently, {user.username}!')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/accounts/login/')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def verification_submit_view(request):
    if request.user.role != 'organiser':
        messages.error(request, 'Only organisers can submit verification documents.')
        return redirect('/')

    if request.user.is_verified:
        messages.info(request, 'Your account is already verified.')
        return redirect('/accounts/profile/')

    if request.method == 'POST':
        form = VerificationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_status = 'pending'
            user.save()
            messages.success(request, 'Document submitted. Awaiting admin review.')
            return redirect('/accounts/profile/')
    else:
        form = VerificationForm(instance=request.user)

    return render(request, 'accounts/verification_submit.html', {'form': form})


@login_required
def verification_status_view(request):
    return render(request, 'accounts/verification_status.html', {'user': request.user})