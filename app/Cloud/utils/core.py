import math
import os
import time
import urllib.parse

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse

from Cloud.models import CloudObject


def get_files_and_dirs(path):
    objects = []
    for it in os.listdir(path):
        curr_path = os.path.join(path, it)
        if it[0] == ".":
            continue
        objects.append(CloudObject(real_path=curr_path))

    return sorted(objects)


def check_permissions(func):
    def wrapper(request, *args, **kwargs):
        path = kwargs["path"] if (len(kwargs) == 1) else ""
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
        if not request.user.is_authenticated:
            return render(
                request,
                "errors/401.html",
                context={
                    "next": reverse("Cloud.open_dir", args=[path])
                    if path != ""
                    else reverse("Cloud.index")
                },
                status=401,
            )
        if not os.path.exists(file_path):
            raise Http404
        if settings.STORAGE_DIRECTORY not in file_path:
            raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrapper


def check_exists(func):
    def wrapper(path, *args, **kwargs):
        file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
        if not os.path.exists(file_path):
            raise Http404
        return func(file_path, *args, **kwargs)

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
    return dirs_count, files_count


def get_properties(path):
    properties = {}
    is_file = os.path.isfile(path)
    properties["Имя"] = os.path.split(path)[1]
    properties["Тип"] = (
        f'Файл "{os.path.splitext(path)[1][1:].upper()}"' if is_file else "Папка"
    )
    properties["Расположение"] = (
        os.path.split(path)[0]
        .replace(settings.STORAGE_DIRECTORY, "")
        .replace("\\", "/")
    )
    properties["Размер"] = convert_size(
        os.path.getsize(path) if is_file else get_dir_size(path)
    )
    if is_file:
        properties["Открыт"] = time.strftime(
            "%d %B %Y %X", time.localtime(os.path.getatime(path))
        )
        properties["Изменен"] = time.strftime(
            "%d %B %Y %X", time.localtime(os.path.getmtime(path))
        )
    else:
        cnt = get_dirs_and_files_count(path)
        properties["Содержит"] = f"Файлов: {cnt[1]}; папок: {cnt[0]}"
    return properties


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}" if i == 0 else f"{s} {size_name[i]} ({size_bytes} B)"


def parse_url(url):
    return os.path.normpath(
        os.path.join(settings.STORAGE_DIRECTORY, urllib.parse.unquote(url))
    )
