import os
import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse

ICONS = {
    'css': 'Cloud/images/format_icons/css.png', 'csv': 'Cloud/images/format_icons/csv.png',
    'dll': 'Cloud/images/format_icons/dll.png', 'doc': 'Cloud/images/format_icons/doc.png',
    'docx': 'Cloud/images/format_icons/doc.png', 'dwg': 'Cloud/images/format_icons/dwg.png',
    'exe': 'Cloud/images/format_icons/exe.png', 'flac': 'Cloud/images/format_icons/flac.png',
    'gif': 'Cloud/images/format_icons/gif.png', 'htm': 'Cloud/images/format_icons/htm.png',
    'html': 'Cloud/images/format_icons/htm.png', 'ico': 'Cloud/images/format_icons/ico.png',
    'iso': 'Cloud/images/format_icons/iso.png', 'jpg': 'Cloud/images/format_icons/jpg.png',
    'json': 'Cloud/images/format_icons/json.png', 'mkv': 'Cloud/images/format_icons/mkv.png',
    'mp3': 'Cloud/images/format_icons/mp3.png', 'mp4': 'Cloud/images/format_icons/mp4.png',
    'pdf': 'Cloud/images/format_icons/pdf.png', 'pkt': 'Cloud/images/format_icons/pkt.png',
    'png': 'Cloud/images/format_icons/png.png', 'ppt': 'Cloud/images/format_icons/ppt.png',
    'pptx': 'Cloud/images/format_icons/ppt.png', 'txt': 'Cloud/images/format_icons/txt.png',
    'wav': 'Cloud/images/format_icons/wav.png', 'xls': 'Cloud/images/format_icons/xls.png',
    'xlsx': 'Cloud/images/format_icons/xls.png', 'xml': 'Cloud/images/format_icons/xml.png',
    'zip': 'Cloud/images/format_icons/zip.png', '7z': 'Cloud/images/format_icons/zip.png'
}


class CloudObject(models.Model):
    real_path = models.CharField(max_length=1023)
    path = models.CharField(max_length=1023)
    name = models.CharField(max_length=255)
    is_file = models.BooleanField()
    ext = models.CharField(max_length=31)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "real_path" not in kwargs:
            return
        path = kwargs["real_path"]
        self.real_path = path
        self.path = path.replace(settings.STORAGE_DIRECTORY, "").replace('\\', '/')
        self.name = os.path.split(path)[1]
        self.is_file = os.path.isfile(path)
        self.ext = os.path.splitext(path)[1][1:].lower()

    def __str__(self):
        return self.path

    def __eq__(self, other):
        return other.path == self.path

    def __lt__(self, other):
        if not self.is_file and other.is_file:
            return True
        if self.is_file and not other.is_file:
            return False
        return self.name < other.name

    def get_absolute_url(self):
        return reverse('open_dir', args=[self.path]) if self.path != "" else reverse('index')

    def get_rel_url(self):
        path = reverse('open_dir', args=[self.path]) if self.path != "" else reverse('index')
        return path[path.find('/', 1) + 1:]

    def get_icon(self):
        if not self.is_file:
            return 'Cloud/images/folder.png'
        return ICONS.get(self.ext, "Cloud/images/file.png")


class Favorites(models.Model):
    obj = models.ForeignKey(CloudObject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Shared(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    obj = models.ForeignKey(CloudObject, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('shared', args=[self.uuid])


class Clipboard(models.Model):
    obj = models.ForeignKey(CloudObject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cut = models.BooleanField(default=False)
