import mimetypes
import os
import shutil
import tempfile
import uuid
import zipfile

from django.conf import settings
from django.http import HttpResponse, JsonResponse

from Cloud.models import CloudObject, Clipboard
from Cloud.utils.core import check_exists, get_dir_size, get_properties


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
    obj = CloudObject(real_path=name)
    return JsonResponse({
        "result": "ok",
        "abs_url": obj.get_absolute_url(),
        "rel_url": obj.get_rel_url(),
        "name": obj.name,
    })


@check_exists
def properties(path):
    return JsonResponse(get_properties(path))


def create_directory(path):
    file_path = os.path.split(path)[0]
    path = os.path.join(file_path, "Новая папка")
    if os.path.exists(path):
        i = 2
        while os.path.exists(path):
            path = os.path.join(file_path, f"Новая папка ({i})")
            i += 1
    os.mkdir(path)
    obj = CloudObject(real_path=path)
    return JsonResponse({
        "result": "ok",
        "name": obj.name,
        "img": "/static/" + obj.get_icon(),
        "rel_url": obj.get_rel_url(),
        "abs_url": obj.get_absolute_url(),
    })


def upload(path, files):
    result = {"files": []}
    for filename, file in files.items():
        name = files[filename].name
        file_path = os.path.join(path, name)
        if os.path.exists(file_path):
            result["files"].append({
                "name": name,
                "exists": "true"
            })
            continue
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        obj = CloudObject(real_path=file_path)
        result["files"].append({
            "name": obj.name,
            "img": "/static/" + obj.get_icon(),
            "rel_url": obj.get_rel_url(),
        })
    result["result"] = "ok"
    return JsonResponse(result)


@check_exists
def copy(path, cut, user):
    Clipboard.objects.filter(user_id=user.id).delete()

    co, _ = CloudObject.objects.get_or_create(real_path=path)
    Clipboard.objects.create(obj=co, user=user, cut=cut)
    return JsonResponse({"result": "ok"})


@check_exists
def paste(path, user):
    co = Clipboard.objects.filter(user_id=user.id)
    if len(co) == 0:
        return JsonResponse({"result": "ok", "files": []})
    result = {"files": []}
    for obj in co:
        if os.path.exists(os.path.join(path, obj.obj.name)):
            result["files"].append({
                "name": obj.obj.name,
                "exists": "true"
            })
            continue
        if obj.obj.is_file:
            shutil.copy2(obj.obj.real_path, path)
            result["files"].append({
                "name": obj.obj.name,
                "img": "/static/" + obj.obj.get_icon(),
                "rel_url": obj.obj.get_rel_url(),
            })
        else:
            new_path = shutil.copytree(obj.obj.real_path, os.path.join(path, obj.obj.name))
            co, _ = CloudObject.objects.get_or_create(real_path=new_path)
            result["files"].append({
                "name": co.name,
                "img": "/static/" + co.get_icon(),
                "rel_url": co.get_rel_url(),
                "abs_url": co.get_absolute_url() if not co.is_file else None
            })
        if obj.cut:
            if obj.obj.is_file:
                os.remove(obj.obj.real_path)
            else:
                shutil.rmtree(obj.obj.real_path)
    result["result"] = "ok"
    return JsonResponse(result)
