import os
import shutil
import mimetypes
import urllib.parse

from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import SuspiciousOperation, PermissionDenied

from Cloud.utils import get_files_and_dirs, check_permissions


@check_permissions
def open_dir(request, path=""):
    file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
    if request.method == "POST":
        raise SuspiciousOperation
    if "action" in request.GET and request.GET["action"] == "Download":
        file_path = urllib.parse.unquote(request.GET["url"])
        return download(file_path)
    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    return render(request, 'Cloud/cloud.html', context={"objects": objects, "current": os.path.split(path)[-1]})


def download(path):
    file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
    if os.path.isdir(file_path):
        raise SuspiciousOperation("Cannot download folder")
    with open(file_path, 'rb') as file:
        mime_type, _ = mimetypes.guess_type(file_path)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.split(file_path)[-1]
        return response
