import os
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from .models import CloudObject


def get_files_and_dirs(path):
    objects = []
    for it in os.listdir(path):
        curr_path = os.path.join(path, it)
        if settings.SYSTEM == 'Windows' and os.stat(curr_path).st_file_attributes & 6 or \
                settings.SYSTEM == 'Linux' and it[0] == '.':
            continue
        objects.append(CloudObject(curr_path))

    return sorted(objects)


def check_permissions(func):
    def wrapper(request, **kwargs):
        path = kwargs['path'] if (len(kwargs) == 1) else ''
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
        if not request.user.is_authenticated:
            return redirect(reverse('login') + '?next=' + reverse('open_dir', args=[path])) \
                if path != "" else redirect(reverse('login') + '?next=' + reverse('index'))
        if not os.path.exists(file_path):
            raise Http404
        if settings.STORAGE_DIRECTORY not in file_path:
            raise PermissionDenied
        return func(request, **kwargs)

    return wrapper


def check_exists(func):
    def wrapper(path):
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
        if not os.path.exists(file_path):
            raise Http404
        return func(file_path)

    return wrapper
