import os
import time
import math

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
    def wrapper(path, *args):
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
        if not os.path.exists(file_path):
            raise Http404
        return func(file_path, *args)

    return wrapper


def get_dir_size(path):
    size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


def get_dirs_and_files_count(path):
    dirs_count = 0
    files_count = 0
    for address, dirs, files in os.walk(path):
        dirs_count += len(dirs)
        files_count += len(files)
    return (dirs_count, files_count)


def get_properties(path):
    properties = {}
    is_file = os.path.isfile(path)
    properties["Имя"] = os.path.split(path)[1]
    properties["Тип"] = f"Файл \"{os.path.splitext(path)[1][1:].upper()}\"" if is_file else "Папка"
    properties["Расположение"] = os.path.split(path)[0].replace(settings.STORAGE_DIRECTORY, "").replace("\\", "/")
    properties["Размер"] = convert_size(os.path.getsize(path) if is_file else get_dir_size(path))
    if not is_file:
        cnt = get_dirs_and_files_count(path)
        properties["Содержит"] = f"Файлов: {cnt[1]}; папок: {cnt[0]}"
    if settings.SYSTEM == 'Windows':
        properties["Создан"] = time.strftime("%d %B %Y %X", time.localtime(os.path.getctime(path)))
    if is_file:
        properties["Открыт"] = time.strftime("%d %B %Y %X", time.localtime(os.path.getatime(path)))
        properties["Изменен"] = time.strftime("%d %B %Y %X", time.localtime(os.path.getmtime(path)))
    return properties


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}" if i == 0 else f"{s} {size_name[i]} ({size_bytes} B)"
