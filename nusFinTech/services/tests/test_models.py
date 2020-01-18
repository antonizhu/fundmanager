from django.test import TestCase

from services.models import ETF
# Create your tests here.
class ETFModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ETF.objects.create(name='ETF 1')

    def test_etfname_label(self):
        etf = ETF.objects.get(id=1)
        name_label = etf._meta.get_field('name').verbose_name
        self.assertEqual(name_label, 'name')

        name_maxlength = etf._meta.get_field('name').max_length
        self.assertEqual(name_maxlength, 50)

    def test_object_name_is_id_space_name(self):
        etf = ETF.objects.get(id=1)
        expected_object_name = f'{etf.id} {etf.name}';
        self.assertEqual(expected_object_name, str(etf))
        