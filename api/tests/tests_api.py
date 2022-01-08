from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APITestCase

from api.models import Event


class StatisticAPITestCase(APITestCase):
    """ Testing endpoint /statistic/ with Methods[GET, POST, DELETE] """
    def test_get_all(self):
        url = "/statistic/"

        Event.objects.create(date="2022-01-01")
        Event.objects.create(date="2022-01-02")
        Event.objects.create(date="2022-01-03")

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_with_from(self):
        url = "/statistic/?from=2022-01-02"

        Event.objects.create(date="2022-01-01")
        Event.objects.create(date="2022-01-02")
        Event.objects.create(date="2022-01-03")

        expected_data = [
            {
                "date": "2022-01-02",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
            {
                "date": "2022-01-03",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
        ]

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, expected_data)

    def test_get_with_from(self):
        url = "/statistic/?to=2022-01-02"

        Event.objects.create(date="2022-01-01")
        Event.objects.create(date="2022-01-02")
        Event.objects.create(date="2022-01-03")

        expected_data = [
            {
                "date": "2022-01-01",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
            {
                "date": "2022-01-02",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
        ]

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, expected_data)

    def test_get_with_from_and_to(self):
        url = "/statistic/?from=2022-01-02&to=2022-01-03"

        Event.objects.create(date="2022-01-01")
        Event.objects.create(date="2022-01-02")
        Event.objects.create(date="2022-01-03")
        Event.objects.create(date="2022-01-04")

        expected_data = [
            {
                "date": "2022-01-02",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
            {
                "date": "2022-01-03",
                "cost": "0.00",
                "clicks": 0,
                "views": 0,
                "cpc": 0.0,
                "cpm": 0.0
            },
        ]

        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, expected_data)

    def test_post_save_with_not_existing_date(self):
        url = "/statistic/"
        request_data = {
            "date": "2022-01-01"
        }
        expected_data = {
            "date": "2022-01-01",
            "cost": "0.00",
            "clicks": 0,
            "views": 0,
        }

        response = self.client.post(url, request_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_post_with_existing_date(self):
        url = "/statistic/"

        Event.objects.create(date="2022-01-01", cost=100, clicks=100, views=100)

        request_data = {
            "date": "2022-01-01",
            "cost": "100.00",
            "clicks": 100,
            "views": 100,
        }
        expected_data = {
            "date": "2022-01-01",
            "cost": "200.00",
            "clicks": 200,
            "views": 200,
        }

        response = self.client.post(url, request_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_delete_all(self):
        url = "/statistic/?from=2022-01-02&to=2022-01-03"

        Event.objects.create(date="2022-01-01")
        Event.objects.create(date="2022-01-02")
        Event.objects.create(date="2022-01-03")
        Event.objects.create(date="2022-01-04")

        response = self.client.delete(url)

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.all().exists(), False)
