from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

import random


def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'registration/register.html',
                          {'error': 'Пользователь с таким именем уже существует'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'registration/register.html',
                          {'error': 'Пользователь с таким адресом электронной почты уже существует'})

        try:
            # Проверяем пароль с использованием встроенных правил проверки
            validate_password(password)
        except ValidationError as e:
            # Если пароль не соответствует правилам, выводим сообщение об ошибке
            error_message = ', '.join(e.messages)
            return render(request, 'registration/register.html', {'error': error_message})

        confirmation_code = random.randint(100000, 999999)

        send_mail(
            'Код подтверждения регистрации',
            f'Ваш код подтверждения: {confirmation_code}',
            None,
            [email],
            fail_silently=False,
        )

        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['confirmation_code'] = confirmation_code

        return redirect('confirm_code')
    else:
        return render(request, 'registration/register.html', {'user': request.user})


def confirm_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')

        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        confirmation_code = request.session.get('confirmation_code')

        if str(confirmation_code) == entered_code:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return redirect('/')
        else:
            # Возвращаем ошибку, если код неверный
            return render(request, 'registration/confirm_code.html', {'error': 'Неверный код подтверждения'})
    else:
        return render(request, 'registration/confirm_code.html', {'user': request.user})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

