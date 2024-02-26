from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

import random

from django.views.decorators.csrf import csrf_protect

from ads.models import UserProfile


@csrf_protect
def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        errors = []

        if password != confirm_password:
            errors.append('Пароли не совпадают')

        if User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким именем уже существует')

        if User.objects.filter(email=email).exists():
            errors.append('Пользователь с таким адресом электронной почты уже существует')

        try:
            validate_password(password)

        except ValidationError as e:
            errors.extend(e.messages)

        if errors:
            return render(request, 'registration/register.html', {'errors': errors})

        confirmation_code = random.randint(100000, 999999)

        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.confirmation_code = confirmation_code
        user_profile.save()

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

        return redirect('confirm_code')
    else:
        return render(request, 'registration/register.html', {'user': request.user})


@csrf_protect
def confirm_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')

        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        request.session.clear()

        user = UserProfile.objects.filter(user__username=username).first()
        if not user:
            user = UserProfile.objects.filter(user__email=email).first()

        if user:
            confirmation_code = user.confirmation_code
            if str(confirmation_code) == entered_code:
                user.user.is_active = True
                user.user.save()
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    return redirect('login')
            else:
                return render(request, 'registration/confirm_code.html', {'error': 'Неверный код подтверждения'})
        else:
            return render(request, 'registration/confirm_code.html', {'error': 'Пользователь не найден'})
    else:
        return render(request, 'registration/confirm_code.html', {'user': request.user})


@csrf_protect
def resend_confirmation_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user and user.is_active:
            return render(request, 'error.html', {'error_messages': 'Ваш аккаунт уже активирован.'})

        if user:
            confirmation_code = random.randint(100000, 999999)

            user_profile = UserProfile.objects.get(user=user)
            user_profile.confirmation_code = confirmation_code
            user_profile.save()

            send_mail(
                'Код подтверждения регистрации',
                f'Ваш новый код подтверждения: {confirmation_code}',
                None,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Новый код подтверждения отправлен на вашу почту.')
            return redirect('confirm_code')
        else:
            messages.error(request, 'Пользователь с такой почтой не найден.')
            return render(request, 'resend_confirmation_code.html')

    else:
        return render(request, 'resend_confirmation_code.html')
