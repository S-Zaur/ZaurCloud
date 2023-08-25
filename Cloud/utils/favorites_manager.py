from django.http import JsonResponse

from Cloud.models import CloudObject, Favorites


def add_favorite(path, user):
    co, _ = CloudObject.objects.get_or_create(real_path=path)
    fv, created = Favorites.objects.get_or_create(obj=co, user=user)
    if not created:
        return JsonResponse({"result": "Already added"})
    return JsonResponse({"result": "ok"})


def delete_favorite(path, user):
    (Favorites.objects.filter(user_id=user.id) & Favorites.objects.filter(
        obj__real_path=path)).delete()
    return JsonResponse({"result": "ok"})
