from django.test import TestCase
from .models import Adult_size

class ModelTesting(TestCase):

    def setup(self):
        self.adult_size = Adult_size.objects.create(name='django')

    def test_store_model(self):
        d = self.adult_size
        self.assertTrue(isinstance(d, Adult_size))