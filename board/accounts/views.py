from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random


def register(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Генерируем случайный код подтверждения
        confirmation_code = random.randint(100000, 999999)
        print(f'{confirmation_code=}')

        # Отправляем код подтверждения на почту
        send_mail(
            'Код подтверждения регистрации',
            f'Ваш код подтверждения: {confirmation_code}',
            None,
            [email],
            fail_silently=False,
        )

        # Сохраняем данные пользователя и код подтверждения в сессии
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['confirmation_code'] = confirmation_code

        # Перенаправляем на страницу ввода кода подтверждения
        return redirect('confirm_code')
    else:
        return render(request, 'registration/register.html', {'user': request.user})


def confirm_code(request):
    if request.method == 'POST':
        # Получаем введенный пользователем код
        entered_code = request.POST.get('code')

        # Получаем данные пользователя и код подтверждения из сессии
        username = request.session.get('username')
        email = request.session.get('email')
        password = request.session.get('password')
        confirmation_code = request.session.get('confirmation_code')

        # Проверяем, совпадает ли введенный код с кодом подтверждения
        if str(confirmation_code) == entered_code:
            # Создаем пользователя
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Аутентификация пользователя после успешной регистрации
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            # Очищаем данные из сессии
            # del request.session['username']
            # del request.session['email']
            # del request.session['password']
            # del request.session['confirmation_code']
            # Перенаправляем на страницу успешной регистрации
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
            # Перенаправляем пользователя на нужную страницу после входа
            return redirect('/')
        else:
            # Если пользователь не найден, выводим сообщение об ошибке
            messages.error(request, 'Неправильное имя пользователя или пароль.')
            return redirect('login')  # Можно указать другое имя маршрута для страницы входа
    else:
        return render(request, 'registration/login.html')


def logout_user(request):
    logout(request)
    return redirect('logout')
