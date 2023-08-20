import os
import uuid
import shutil
import zipfile
import tempfile
import mimetypes
import urllib.parse

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import SuspiciousOperation

from Cloud.utils import get_files_and_dirs, check_permissions, check_exists, get_dir_size, get_properties


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
        if action == "Properties":
            return properties(file_path)
        raise SuspiciousOperation

    if os.path.isfile(file_path):
        raise SuspiciousOperation("Cannot open files")
    objects = get_files_and_dirs(file_path)
    return render(request, 'Cloud/cloud.html', context={"objects": objects, "current": os.path.split(path)[-1]})


@check_exists
def download(path):
    if os.path.isdir(path):
        if get_dir_size(path) > 1e9:
            return JsonResponse({"result": "Downloadable object too large"}, status=403)
        zip_file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()) + ".zip")
        with zipfile.ZipFile(zip_file_name, 'w') as zipObj:
            for folderName, subFolders, filenames in os.walk(path):
                for subFolder in subFolders:
                    zipObj.mkdir(subFolder)
                for filename in filenames:
                    file_path = os.path.join(folderName, filename)
                    zipObj.write(file_path, os.path.relpath(file_path, path))
        return download(zip_file_name)
    with open(path, 'rb') as file:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(file, content_type=mime_type)
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % os.path.split(path)[-1]
        return response


@check_exists
def delete(path):
    if settings.DEBUG:
        return JsonResponse({"result": "DEBUG"}, status=403)
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
    return JsonResponse({"result": "ok"})


@check_exists
def rename(path, name):
    name = os.path.join(os.path.split(path)[0], name)
    os.rename(path, name)
    return JsonResponse({"result": "ok"})


@check_exists
def properties(path):
    return JsonResponse(get_properties(path))
