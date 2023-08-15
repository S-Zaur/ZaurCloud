from django.conf import settings
from django.shortcuts import render
import os

from Cloud.utils import get_files_and_dirs, check_permissions


@check_permissions
def open_dir(request, path=""):
    file_path = os.path.normpath(os.path.join(settings.STORAGE_DIRECTORY, path))
    objects = get_files_and_dirs(file_path)
    return render(request, 'Cloud/cloud.html', context={"objects": objects, "current": os.path.split(path)[-1]})
