from django.conf import settings
import os


class CloudObject:
    def __init__(self, path):
        self._real_path = path
        self.path = path.replace(settings.STORAGE_DIRECTORY, "").replace('\\', '/')
        self.name = os.path.split(path)[1]
        self.IS_FILE = os.path.isfile(path)

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return other.path == self.path

    def __lt__(self, other):
        if not self.IS_FILE and other.IS_FILE:
            return True
        if self.IS_FILE and not other.IS_FILE:
            return False
        return self.name < other.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('open_dir', args=[self.path])

    def get_icon(self):
        return 'Cloud/images/file.png' if self.IS_FILE else 'Cloud/images/folder.png'
