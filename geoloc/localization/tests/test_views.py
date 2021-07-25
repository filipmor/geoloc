from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from geoloc.localization.models import Localization

class LocalizationViewTest(APITestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test1234'
        self.email = 'test@test.com'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

        self.localization_output_data = {
            "city": "Los Angeles",
            "continent_code": "NA",
            "continent_name": "North America",
            "country_code": "US",
            "country_name": "United States",
            "id": 1,
            "ip": "134.201.250.155",
            "latitude": 34.0655517578125,
            "longitude": -118.24053955078125,
            "region_code": "CA",
            "region_name": "California",
            "zip_code": "90012"
        }
        self.ip_address = '134.201.250.155'
        self.jwt_url = reverse('token_obtain_pair')
        self.localization_url = reverse('ipstack-localization')
        

    def test_active_user(self):
        self.assertEqual(self.user.is_active, 1, 'Active User')

    def test_jwt_authorization_on_non_existing_user(self):
        response = self.client.post(self.jwt_url, data={'username': 'test2', 'password': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_authorization_on_existing_user(self):
        response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_no_authorization(self):
        response = self.client.post(self.localization_url, data={'ip_address': self.ip_address})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_authorization(self):
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.post(self.localization_url, data={'ip_address': self.ip_address}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_missing_ip(self):
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.post(self.localization_url, **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_wrong_ip(self):
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.post(self.localization_url, data={'ip_address': '00.00.001.0'}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_206_PARTIAL_CONTENT)

    def test_post_database_save(self):
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.post(self.localization_url, data={'ip_address': self.ip_address}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Localization.objects.count(), 1)
        localization_object = Localization.objects.get(ip=self.localization_output_data['ip'])
        self.assertEqual(localization_object.city, self.localization_output_data['city'])

    def test_delete_nonexisting_object(self):
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.delete(self.localization_url, data={'ip_address': '00.00.00.00'}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_existing_object(self):
        # Post object to the database
        jwt_response = self.client.post(self.jwt_url, data={'username': self.username, 'password': self.password})
        self.assertEqual(jwt_response.status_code, status.HTTP_200_OK)
        access_token = jwt_response.json()['access']
        response = self.client.post(self.localization_url, data={'ip_address': self.ip_address}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Localization.objects.count(), 1)
        localization_object = Localization.objects.get(ip=self.localization_output_data['ip'])
        self.assertEqual(localization_object.city, self.localization_output_data['city'])

        # Get object from the database
        response = self.client.delete(self.localization_url, data={'ip_address': self.ip_address}, 
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)