from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def registration_complete(strategy, details, backend, user=None, *args, **kwargs):
    if not user:
        return
    if user.is_active and not kwargs.get('is_new'):
        return
    user.is_active = False
    user.save()
    messages.info(kwargs.get('request'), 'Set a password and confirm email to complete registration')
    return redirect(reverse('register-complete', args=[user.id]))
