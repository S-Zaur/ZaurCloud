import os
import shutil
import mimetypes
import urllib.parse

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import SuspiciousOperation, PermissionDenied

from Cloud.utils import get_files_and_dirs, check_permissions, check_exists


@check_permissions
def open_dir(request, path=""):
    file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
    if request.method == "POST":
        if "action" not in request.POST:
            raise SuspiciousOperation
        action = request.POST["action"]
        file_path = urllib.parse.unquote(request.POST["url"])
        if action == "Delete":
            return delete(file_path)
        if action == "Rename":
            return rename(file_path, request.POST["new_name"])
        raise SuspiciousOperation

    if "action" in request.GET:
        action = request.GET["action"]
        file_path = urllib.parse.unquote(request.GET["url"])
        if action == "Download":
            return download(file_path)
        raise SuspiciousOperation

    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    return render(request, 'Cloud/cloud.html', context={"objects": objects, "current": os.path.split(path)[-1]})


@check_exists
def download(path):
    if os.path.isdir(path):
        raise SuspiciousOperation("Cannot download folder")
    with open(path, 'rb') as file:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.split(path)[-1]
        return response


@check_exists
def delete(path):
    if settings.DEBUG:
        raise PermissionDenied("to remove it, set DEBUG=False")
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    return JsonResponse({"result": "deleted"})


@check_exists
def rename(path, name):
    name = os.path.join(os.path.split(path)[0], name)
    os.rename(path, name)
    return JsonResponse({"result": "ok"})
