from django.test import TestCase

from api.serializers import StatisticSerializer


class SerializersTestCase(TestCase):
    def test_date_validation(self):
        data_invalid_date_field = {"date": "qwerty"}
        serializer = StatisticSerializer(data=data_invalid_date_field)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("date", serializer.errors)

    def test_with_cost_is_not_number(self):
        data_with_cost_as_str = {"date": "2022-01-01", "cost": "one"}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("cost", serializer.errors)
        self.assertEqual(serializer.errors['cost'][0], "A valid number is required.")

    def test_with_clicks_is_not_number(self):
        data_with_cost_as_str = {"date": "2022-01-01", "clicks": "one"}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("clicks", serializer.errors)
        self.assertEqual(serializer.errors['clicks'][0], "A valid integer is required.")

    def test_with_views_is_not_number(self):
        data_with_cost_as_str = {"date": "2022-01-01", "views": "one"}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("views", serializer.errors)
        self.assertEqual(serializer.errors['views'][0], "A valid integer is required.")

    def test_with_clicks_is_float(self):
        data_with_cost_as_str = {"date": "2022-01-01", "clicks": 1.5}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("clicks", serializer.errors)
        self.assertEqual(serializer.errors["clicks"][0], "A valid integer is required.")

    def test_with_views_is_float(self):
        data_with_cost_as_str = {"date": "2022-01-01", "views": 1.5}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("views", serializer.errors)
        self.assertEqual(serializer.errors["views"][0], "A valid integer is required.")

    def test_with_cost_is_negative_integer(self):
        data_with_cost_as_str = {"date": "2022-01-01", "cost": -1}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("cost", serializer.errors)
        self.assertEqual(serializer.errors["cost"][0], "Ensure this value is greater than or equal to 0.")

    def test_with_clicks_is_negative_integer(self):
        data_with_cost_as_str = {"date": "2022-01-01", "clicks": -1}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("clicks", serializer.errors)
        self.assertEqual(serializer.errors["clicks"][0], "Ensure this value is greater than or equal to 0.")

    def test_with_views_is_negative_integer(self):
        data_with_cost_as_str = {"date": "2022-01-01", "views": -1}
        serializer = StatisticSerializer(data=data_with_cost_as_str)

        self.assertEqual(serializer.is_valid(), False)
        self.assertIn("views", serializer.errors)
        self.assertEqual(serializer.errors["views"][0], "Ensure this value is greater than or equal to 0.")
