import math
import random
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegistrationForm, LoginForm
from .models import OtpModel
from .tokens import account_activation_token


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return render(request, 'registration/register_done.html', {'new_user': user})
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'user_form': form})


def activate_email(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('registration/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if not email.send():
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activate_done.html')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            OtpModel.objects.filter(user=user).delete()
            if user is not None:
                if user.is_active:
                    otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider())
                    send_otp_in_mail(user, otp_stuff)
                    return redirect(reverse('otp'))
                else:
                    messages.error(request, 'Disabled account')
            else:
                messages.error(request, 'Incorrect login or password')
        else:
            messages.error(request, form.errors)
    return render(request, 'registration/login.html')


def send_otp_in_mail(user, otp):
    subject = 'Otp for signin'
    message = f'Hi {user.username}, here we sent otp for secure login \n Otp is - {otp.otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)


def otp_provider():
    corpus = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    generate_OTP = ""
    size = 7
    length = len(corpus)
    for i in range(size):
        generate_OTP += corpus[math.floor(random.random() * length)]
    return generate_OTP


def otp_verify_view(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        verify_otp = OtpModel.objects.filter(otp=otp).first()
        if verify_otp is not None:
            if timezone.now() - verify_otp.created_at > timedelta(seconds=settings.OTP_TIMEOUT):
                messages.error(request, "The otp has expired")
                verify_otp.delete()
                verify_otp.save()
                return redirect(reverse('login'))

            login(request, verify_otp.user)
            verify_otp.delete()
            verify_otp.save()
            return redirect(reverse('index'))
        else:
            messages.error(request, "Invalid otp!")
            return redirect(reverse('otp'))
    else:
        return render(request, 'registration/otp.html')
