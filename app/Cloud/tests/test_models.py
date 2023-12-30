import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from Cloud.models import CloudObject, Favorites, Shared


class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        o = CloudObject.objects.create(id=101, real_path="/app/Cloud/tests")
        o2 = CloudObject.objects.create(id=102, real_path="/app/Cloud/templates")
        CloudObject.objects.create(
            id=103, real_path="/app/Cloud/static/Cloud/images/file.png"
        )
        CloudObject.objects.create(id=104, real_path="/app/Cloud/tests/test_api.py")
        u = User.objects.create_user(username="testuser", password="12345")
        Favorites.objects.create(id=101, obj=o, user=u)
        s = Shared.objects.create(obj=o, uuid="0074d6ed-cdf6-4d97-85aa-678dcf0197a0")
        Shared.objects.create(
            obj=o2, parent=s, uuid="0074d6ed-cdf6-4d97-85aa-678dcf0197a1"
        )

    def test_cloud_object_labels(self):
        co = CloudObject.objects.get(id=101)
        label = co._meta.get_field("real_path").verbose_name
        self.assertEquals(label, "real path")
        label = co._meta.get_field("path").verbose_name
        self.assertEquals(label, "path")
        label = co._meta.get_field("name").verbose_name
        self.assertEquals(label, "name")
        label = co._meta.get_field("is_file").verbose_name
        self.assertEquals(label, "is file")
        label = co._meta.get_field("ext").verbose_name
        self.assertEquals(label, "ext")

    def test_cloud_object_max_lengths(self):
        co = CloudObject.objects.get(id=101)
        max_length = co._meta.get_field("real_path").max_length
        self.assertEquals(max_length, 1023)
        max_length = co._meta.get_field("path").max_length
        self.assertEquals(max_length, 1023)
        max_length = co._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)
        max_length = co._meta.get_field("ext").max_length
        self.assertEquals(max_length, 31)

    def test_cloud_object_fields(self):
        co = CloudObject.objects.get(id=101)
        self.assertEqual(co.real_path, "/app/Cloud/tests")
        self.assertEqual(co.path, "/app/Cloud/tests")
        self.assertEqual(co.name, "tests")
        self.assertFalse(co.is_file)
        self.assertEqual(co.ext, "")
        co = CloudObject.objects.get(id=103)
        self.assertTrue(co.is_file)
        self.assertEqual(co.ext, "png")

    def test_cloud_object_to_string(self):
        co = CloudObject.objects.get(id=101)
        self.assertEqual(str(co), "/app/Cloud/tests")

    def test_cloud_object_urls(self):
        co = CloudObject.objects.get(id=101)
        self.assertEqual(co.get_absolute_url(), "/cloud//app/Cloud/tests")
        self.assertEqual(co.get_rel_url(), "/app/Cloud/tests")
        co = CloudObject(path="")
        self.assertEqual(co.get_absolute_url(), "/cloud/")
        self.assertEqual(co.get_rel_url(), "")

    def test_cloud_object_eq(self):
        co = CloudObject.objects.get(id=101)
        co2 = CloudObject(real_path="/app/Cloud/tests")
        co3 = CloudObject.objects.get(id=102)
        self.assertEqual(co, co2)
        self.assertNotEqual(co, co3)

    def test_cloud_object_lt(self):
        objs = CloudObject.objects.filter(id__gt=100)
        self.assertFalse(objs[0] < objs[1])
        self.assertTrue(objs[2] < objs[3])
        self.assertTrue(objs[0] < objs[2])
        self.assertFalse(objs[3] < objs[1])

    def test_cloud_object_icons(self):
        objs = CloudObject.objects.all()
        self.assertEqual(objs[0].get_icon(), "Cloud/images/folder.png")
        self.assertEqual(objs[2].get_icon(), "Cloud/images/format_icons/png.png")
        self.assertEqual(objs[3].get_icon(), "Cloud/images/file.png")

    def test_shared(self):
        shared = Shared.objects.first()
        self.assertEqual(shared._meta.get_field("uuid").verbose_name, "uuid")
        self.assertEqual(shared._meta.get_field("parent").verbose_name, "parent")
        self.assertEqual(shared._meta.get_field("obj").verbose_name, "obj")
        self.assertEqual(shared.obj, CloudObject.objects.get(id=101))
        self.assertEqual(shared.uuid, uuid.UUID("0074d6ed-cdf6-4d97-85aa-678dcf0197a0"))
        self.assertIsNone(shared.parent)
        self.assertEqual(
            shared.get_absolute_url(),
            "/cloud/shared/0074d6ed-cdf6-4d97-85aa-678dcf0197a0",
        )
        shared2 = Shared.objects.last()
        self.assertEqual(shared2.parent, shared)

    def test_favorite(self):
        f = Favorites.objects.get(id=101)
        self.assertEqual(f._meta.get_field("obj").verbose_name, "obj")
        self.assertEqual(f._meta.get_field("user").verbose_name, "user")
        self.assertEqual(f.user, User.objects.first())
        self.assertEqual(f.obj, CloudObject.objects.get(id=101))
