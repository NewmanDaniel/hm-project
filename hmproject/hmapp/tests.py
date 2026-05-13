from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Device, Payload

class PayloadModelTests(TestCase):
    def test_unique_fcnt_constraint(self):
        device = Device.objects.create(devEUI="test1234")
        Payload.objects.create(device=device, fCnt=1, data_raw="AQ==", data_hex="01", is_passing=True)

        with self.assertRaises(Exception):
            # This should raise IntegrityError due to unique constraint
            Payload.objects.create(device=device, fCnt=1, data_raw="AA==", data_hex="00", is_passing=False)

class PayloadAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.ingest_url = '/api/payloads/'

    def test_ingest_passing_payload(self):
        data = {
            "fCnt": 100,
            "devEUI": "abcdabcdabcdabcd",
            "data": "AQ==" # Decodes to 01
        }
        response = self.client.post(self.ingest_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Device.objects.filter(devEUI="abcdabcdabcdabcd").exists())
        payload = Payload.objects.first()
        self.assertTrue(payload.is_passing)
        self.assertEqual(payload.data_hex, '01')

    def test_ingest_failing_payload(self):
        data = {
            "fCnt": 101,
            "devEUI": "abcdabcdabcdabcd",
            "data": "AA==" # Decodes to 00
        }
        response = self.client.post(self.ingest_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payload = Payload.objects.get(fCnt=101)
        self.assertFalse(payload.is_passing)

    def test_duplicate_fcnt_rejection(self):
        data = {
            "fCnt": 200,
            "devEUI": "dupdevice",
            "data": "AQ=="
        }
        # First request
        self.client.post(self.ingest_url, data, format='json')
        # Second request (same fCnt)
        response = self.client.post(self.ingest_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Duplicate', str(response.data))
