import io
import os
import shutil
import unittest
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from Cloud.models import Favorites, Shared

GET_PAGES = [
    "/cloud/download/",
    "/cloud/properties/",
    "/cloud/favorites/",
    "/cloud/shared/all/",
    "/cloud/goto/",
]
POST_PAGES = [
    "/cloud/upload/",
    "/cloud/create-ditectory/",
    "/cloud/copy/",
    "/cloud/paste/",
    "/cloud/delete/",
    "/cloud/rename/",
    "/cloud/add-favorite/",
    "/cloud/remove-favorite/",
    "/cloud/create-link/",
    "/cloud/delete-link/",
]


class APITestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="testuser", password="12345")

    @classmethod
    def setUpClass(cls):
        dirs = [
            settings.STORAGE_DIRECTORY + "/download",
            settings.STORAGE_DIRECTORY + "/copypaste",
            settings.STORAGE_DIRECTORY + "/delete",
            settings.STORAGE_DIRECTORY + "/rename_me",
            settings.STORAGE_DIRECTORY + "/favorite",
            settings.STORAGE_DIRECTORY + "/share",
        ]
        files = [
            settings.STORAGE_DIRECTORY + "/download/readme.txt",
            settings.STORAGE_DIRECTORY + "/copy.txt",
            settings.STORAGE_DIRECTORY + "/cut.txt",
            settings.STORAGE_DIRECTORY + "/delete/delete.txt",
            settings.STORAGE_DIRECTORY + "/delete/please_dont_delete.txt",
            settings.STORAGE_DIRECTORY + "/rename_me/rename_me.txt",
            settings.STORAGE_DIRECTORY + "/favorite/favorite.txt",
            settings.STORAGE_DIRECTORY + "/share/share.txt",
        ]
        for dir in dirs:
            os.mkdir(dir)
        for file in files:
            with open(file, "w") as f:
                f.write("Create a new text file!")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.STORAGE_DIRECTORY)
        return super().tearDownClass()

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_401(self):
        self.client.logout()
        self.assertEqual(self.client.get("/cloud/").status_code, 401)
        for i in GET_PAGES:
            with self.subTest("Test unauthorized", i=i):
                self.assertEqual(self.client.get(i).status_code, 401)
        for i in POST_PAGES:
            with self.subTest("Test unauthorized", i=i):
                self.assertEqual(self.client.post(i).status_code, 401)

    def test_404(self):
        self.assertEqual(
            self.client.get(
                "/cloud/this/path/definitely/does/not/exist",
            ).status_code,
            404,
        )
        for i in GET_PAGES:
            with self.subTest("Test not found", i=i):
                self.assertEqual(
                    self.client.get(
                        i,
                        {"url": "this/path/definitely/does/not/exist"},
                    ).status_code,
                    404,
                )
        for i in POST_PAGES:
            with self.subTest("Test not found", i=i):
                if i in ["/cloud/delete-link/"]:
                    continue
                self.assertEqual(
                    self.client.post(
                        i,
                        {
                            "url": "this/path/definitely/does/not/exist",
                            "cut": False,
                            "new-name": "name",
                        },
                    ).status_code,
                    404,
                )

    def test_upload(self):
        with open("/app/Cloud/static/Cloud/images/file.png", "rb") as file:
            r = self.client.post("/cloud/upload/", {"url": "", "files": file})
            self.assertEqual(r.status_code, 200)
            self.assertTrue(
                os.path.exists(os.path.join(settings.STORAGE_DIRECTORY, "file.png"))
            )
            res_json = r.json()
            self.assertEqual(res_json["files"][0]["name"], "file.png")
            self.assertEqual(
                res_json["files"][0]["img"], "/static/Cloud/images/format_icons/png.png"
            )
            self.assertEqual(res_json["files"][0]["rel_url"], "file.png")

    def test_download(self):
        r = self.client.get("/cloud/download/", {"url": "download"})
        self.assertEqual(r.status_code, 200)
        self.assertRegex(
            r.get("Content-Disposition"),
            r"attachment; filename=[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\.zip",
        )
        with io.BytesIO(r.content) as buf_bytes:
            self.assertEqual(buf_bytes.getbuffer().nbytes, 141)
        r = self.client.get("/cloud/download/", {"url": "download/readme.txt"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.get("Content-Disposition"),
            "attachment; filename=readme.txt",
        )
        with io.BytesIO(r.content) as buf_bytes:
            self.assertEqual(buf_bytes.getbuffer().nbytes, 23)

    def test_properties(self):
        r = self.client.get("/cloud/properties/", {"url": "download"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(),
            {
                "Имя": "download",
                "Размер": "23.0 B",
                "Расположение": "",
                "Содержит": "Файлов: 1; папок: 0",
                "Тип": "Папка",
            },
        )
        r = self.client.get("/cloud/properties/", {"url": "download/readme.txt"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["Имя"], "readme.txt")
        self.assertEqual(r.json()["Тип"], 'Файл "TXT"')
        self.assertEqual(r.json()["Расположение"], "/download")
        self.assertEqual(r.json()["Размер"], "23.0 B")

    def test_copy_paste(self):
        r = self.client.post("/cloud/copy/", {"url": "copy.txt", "cut": False})
        self.assertEqual(r.status_code, 200)
        r = self.client.post("/cloud/paste/", {"url": "copypaste"})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            os.path.exists(settings.STORAGE_DIRECTORY + "/copypaste/copy.txt")
        )
        self.assertTrue(os.path.exists(settings.STORAGE_DIRECTORY + "/copy.txt"))
        res_json = r.json()
        self.assertEqual(res_json["files"][0]["name"], "copy.txt")
        self.assertEqual(
            res_json["files"][0]["img"], "/static/Cloud/images/format_icons/txt.png"
        )
        self.assertEqual(res_json["files"][0]["rel_url"], "copypaste/copy.txt")

    def test_cut_paste(self):
        r = self.client.post("/cloud/copy/", {"url": "cut.txt", "cut": True})
        self.assertEqual(r.status_code, 200)
        r = self.client.post("/cloud/paste/", {"url": "copypaste"})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            os.path.exists(settings.STORAGE_DIRECTORY + "/copypaste/cut.txt")
        )
        self.assertFalse(os.path.exists(settings.STORAGE_DIRECTORY + "/cut.txt"))

    def test_delete(self):
        r = self.client.post("/cloud/delete/", {"url": "delete/delete.txt"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(
            os.path.exists(settings.STORAGE_DIRECTORY + "/delete/delete.txt")
        )
        r = self.client.post("/cloud/delete/", {"url": "delete"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(os.path.exists(settings.STORAGE_DIRECTORY + "/delete"))

    def test_rename(self):
        r = self.client.post(
            "/cloud/rename/",
            {"url": "rename_me/rename_me.txt", "new-name": "ok.txt"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(
            os.path.exists(settings.STORAGE_DIRECTORY + "/rename_me/rename_me.txt")
        )
        self.assertTrue(
            os.path.exists(settings.STORAGE_DIRECTORY + "/rename_me/ok.txt")
        )
        r = self.client.post(
            "/cloud/rename/",
            {"url": "rename_me", "new-name": "ok"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertFalse(os.path.exists(settings.STORAGE_DIRECTORY + "/rename_me"))
        self.assertTrue(os.path.exists(settings.STORAGE_DIRECTORY + "/ok"))

    def test_rename_400(self):
        r = self.client.post(
            "/cloud/rename/",
            {"url": "download", "new-name": ""},
        )
        self.assertEqual(r.status_code, 400)
        r = self.client.post(
            "/cloud/rename/",
            {"url": "download", "new-name": ".download"},
        )
        self.assertEqual(r.status_code, 400)

    def test_create_directory(self):
        r = self.client.post("/cloud/create-directory/", {"url": "", "in-place": True})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(os.path.exists(settings.STORAGE_DIRECTORY + "/Новая папка"))
        res_json = r.json()
        self.assertEqual(res_json["name"], "Новая папка")
        self.assertEqual(res_json["img"], "/static/Cloud/images/folder.png")
        self.assertEqual(
            res_json["rel_url"],
            "%D0%9D%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BF%D0%BA%D0%B0",
        )
        self.assertEqual(
            res_json["abs_url"],
            "/cloud/%D0%9D%D0%BE%D0%B2%D0%B0%D1%8F%20%D0%BF%D0%B0%D0%BF%D0%BA%D0%B0",
        )

    def test_favorites(self):
        count_before = Favorites.objects.count()
        r = self.client.post("/cloud/add-favorite/", {"url": "favorite/favorite.txt"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"result": "ok"})
        self.assertEqual(Favorites.objects.count(), count_before + 1)
        r = self.client.post("/cloud/add-favorite/", {"url": "favorite/favorite.txt"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"result": "Already added"})
        self.assertEqual(Favorites.objects.count(), count_before + 1)
        r = self.client.post(
            "/cloud/remove-favorite/", {"url": "favorite/favorite.txt"}
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"result": "ok"})
        self.assertEqual(Favorites.objects.count(), count_before)

    def test_share(self):
        count_before = Shared.objects.count()
        r = self.client.post("/cloud/create-link/", {"url": "share"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["result"], "ok")
        self.assertRegex(
            r.json()["url"],
            "/cloud/shared/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        )
        uuid = r.json()["url"].split("/")[3]
        self.assertEqual(Shared.objects.count(), count_before + 2)
        r = self.client.post("/cloud/delete-link/", {"uuid": uuid})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["result"], "ok")
        self.assertEqual(Shared.objects.count(), count_before)
