import os

from django.http import JsonResponse
from django.urls import reverse

from Cloud.models import CloudObject, Shared


def share(path):
    co, _ = CloudObject.objects.get_or_create(real_path=path)
    res, _ = Shared.objects.get_or_create(obj_id=co.id)
    if co.is_file:
        return JsonResponse({"result": "ok", "url": reverse("shared", args=[res.uuid])})
    for addr, dirs, files in os.walk(path):
        s = Shared.objects.get(obj__real_path=addr)
        for directory in dirs:
            co, _ = CloudObject.objects.get_or_create(real_path=os.path.join(addr, directory))
            Shared.objects.get_or_create(obj=co, parent=s)
        for file in files:
            co, _ = CloudObject.objects.get_or_create(real_path=os.path.join(addr, file))
            Shared.objects.get_or_create(obj=co, parent=s)
    return JsonResponse({"result": "ok", "url": reverse("shared", args=[res.uuid])})


def unshare(path):
    Shared.objects.get(obj__real_path=path).delete()
    return JsonResponse({"result": "ok"})
