from django.test import TestCase

from rest_framework.exceptions import ParseError

from api.validators import validate_date_format


class APITestCase(TestCase):
    def test_validate_date_format(self):
        invalid_date = "01-01-2022"
        with self.assertRaises(ParseError):
            validate_date_format(invalid_date)
