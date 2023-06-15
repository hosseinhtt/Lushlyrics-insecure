from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .decorators import send_forget_password_mail
import uuid


def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('default')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'default')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'user/login.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registrationPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, "user/signup.html", context)


def forgot_password(request):
    try:
        if request.method == 'POST':
            email_user = request.POST.get('email')

            if not User.objects.filter(email=email_user):
                messages.info(request, "User with email is not exists")
                return redirect('forgot_password')
            else:
                token = str(uuid.uuid4())
                user_obj = User.objects.get(email=email_user)
                send_forget_password_mail(user_obj, token)
                messages.info(
                    request, "Check your email for password recovery link")
                return redirect('login')
    except Exception as e:
        print(e)
    return render(request, "user/forget-password.html")


def change_password(request, id):
    user_obj = User.objects.get(id=id)
    if request.method == 'POST':
        new_password = request.POST.get('pass1')
        confirm_password = request.POST.get('pass2')

        if len(new_password) < 8:
            messages.info(
                request, 'Your password must consist of at least 8 characters!')
            return redirect(f'change-password/{id}')

        elif new_password != confirm_password:
            messages.info(request, 'Password don\'t match')
            return redirect(f'change-password/{id}')

        user_obj.set_password(new_password)
        user_obj.save()
        messages.info(request, 'Password has been renewd sucessfully')
        return redirect('login')
    return render(request, 'user/change-password.html')
