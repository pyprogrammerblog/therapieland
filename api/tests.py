from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TinyURL, TinyURLStats
from faker import Faker
import factory
from factory.fuzzy import FuzzyInteger

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User


class TinyURLFactory(factory.django.DjangoModelFactory):
    url = "https://stackoverflow.com"
    shortcode = "abc"

    class Meta:
        model = TinyURL


class TinyURLStatsFactory(factory.django.DjangoModelFactory):
    shortcode = factory.SubFactory(TinyURLFactory)
    year = 2020
    week = FuzzyInteger(1, 52)

    class Meta:
        model = TinyURLStats


# Create your tests here.
class TinyUrlsTestCase(APITestCase):
    def setUp(self):
        user = UserFactory()
        self.client.login(username=user.username, password=user.password)
        self.url_list = reverse("urls-list")

    def test_post_url(self):
        data = {"url": "https://stackoverflow.com"}
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('url', response.json())
        self.assertIn("shortcode", response.json())

    def test_post_url_shortcode(self):
        data = {"url": "https://stackoverflow.com", "shortcode": "abc"}
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('url', response.json())
        self.assertEqual(response.json()["shortcode"], data["shortcode"])

    def test_post_url_409(self):
        TinyURLFactory.create()
        data = {"url": "https://stackoverflow.com", "shortcode": "abc"}
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json(), 'Shortcode already in use')

    def test_post_url_400(self):
        response = self.client.post(self.url_list, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_shortcode(self):
        obj = TinyURLFactory.create()
        self.url_detail = reverse("urls-detail", args=(obj.shortcode,))
        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_shortcode_404(self):
        self.url_detail = reverse("urls-detail", args=("something",))
        response = self.client.get(self.url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TinyUrlsStatsTestCase(APITestCase):

    def setUp(self):
        user = UserFactory()
        self.client.login(username=user.username, password=user.password)

    def test_get_stats(self):
        obj = TinyURLFactory.create()
        url_detail = reverse("urls-detail", args=(obj.shortcode,))
        self.client.get(url_detail, format='json')
        url_stats = reverse("urls-stats", args=(obj.shortcode,))
        response = self.client.get(url_stats, format='json')
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['redirects_count'], 1)

    def test_get_more_stats(self):
        obj = TinyURLFactory.create()
        [TinyURLStatsFactory.create(
            shortcode=obj, week=week, year=2020
        ) for _ in range(10) for week in range(1, 11)]
        url_stats = reverse("urls-stats", args=(obj.shortcode,))
        response = self.client.get(url_stats, format='json')
        self.assertEqual(len(response.json()), 10)
        self.assertEqual(response.json()[0]['redirects_count'], 10)
        self.assertEqual(
            response.json()[0], {'year': 2020, 'week': 1, 'redirects_count': 10}
        )
        self.assertEqual(
            response.json()[-1], {'year': 2020, 'week': 10, 'redirects_count': 10}
        )
