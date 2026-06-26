from django.test import TestCase

class WSGITest(TestCase):
    def test_wsgi_application(self):
        from config.wsgi import application
        self.assertIsNotNone(application)

class ASGITest(TestCase):
    def test_asgi_application(self):
        from config.asgi import application
        self.assertIsNotNone(application)