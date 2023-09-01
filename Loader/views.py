import os.path

from celery_progress.views import get_progress
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Loader.tasks import download


@login_required
def progress_view(request):
    if 'url' in request.GET:
        result = download.delay(request.GET['url'], os.path.join(settings.STORAGE_DIRECTORY, request.GET['path']))
        return render(request, 'display_progress.html', context={'task_id': result.task_id})
    return render(request, 'display_progress.html')


@login_required
def task_status(request, task_id):
    return get_progress(request, task_id)
