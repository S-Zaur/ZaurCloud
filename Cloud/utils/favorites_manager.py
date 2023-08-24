from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from Cloud.models import CloudObject, Favorites


def add_favorite(path, user):
    try:
        co = CloudObject.objects.get(_real_path=path)
    except ObjectDoesNotExist:
        co = CloudObject(path=path)
        co.save()
    fv, created = Favorites.objects.get_or_create(obj=co, user=user)
    if not created:
        return JsonResponse({"result": "Already added"})
    return JsonResponse({"result": "ok"})


def delete_favorite(path, user):
    (Favorites.objects.filter(user_id=user.id) & Favorites.objects.filter(
        obj___real_path=path)).delete()
    return JsonResponse({"result": "ok"})
