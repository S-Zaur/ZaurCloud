from django.conf import settings
import os


class CloudObject:
    __icons = {
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

    def __init__(self, path):
        self._real_path = path
        self.path = path.replace(settings.STORAGE_DIRECTORY, "").replace('\\', '/')
        self.name = os.path.split(path)[1]
        self.IS_FILE = os.path.isfile(path)
        self.EXT = os.path.splitext(path)[1][1:].lower()

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

    def get_rel_url(self):
        from django.urls import reverse
        path = reverse('open_dir', args=[self.path])
        return path[path.find('/',1):]

    def get_icon(self):
        if not self.IS_FILE:
            return 'Cloud/images/folder.png'
        return self.__icons.get(self.EXT, "Cloud/images/file.png")
