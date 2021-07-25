from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LocalizationSerializer
from .models import Localization
import requests
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import os

class LocalizationView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LocalizationSerializer

    def post(self, request, format=None):

        if "ip_address" in request.data:
            # External GET query to access corresponding geolocalization, if exists
            try:
                response = requests.get('http://api.ipstack.com/'+request.data['ip_address']+'?access_key=' + os.environ['IPSTACK_ACCESS_KEY'])
                ip_localization = response.json()
                data = {
                    'ip': ip_localization['ip'],
                    'continent_code': ip_localization['continent_code'],
                    'continent_name': ip_localization['continent_name'],
                    'country_code': ip_localization['country_code'],
                    'country_name': ip_localization['country_name'],
                    'region_code': ip_localization['region_code'],
                    'region_name': ip_localization['region_name'],
                    'city': ip_localization['city'],
                    'zip_code': ip_localization['zip'],
                    'latitude': ip_localization['latitude'],
                    'longitude': ip_localization['longitude']
                }

                # Check if localization exists for the given IP
                serializer = LocalizationSerializer(data=data)
                if not serializer.is_valid():
                    return Response("Localization does not exists for the given IP", status=status.HTTP_206_PARTIAL_CONTENT)

                # If localication exists, add (or update) the database
                obj = Localization.objects.filter(ip=ip_localization['ip'])
                if not obj:
                    serializer.save()
                return Response("Localization added to the database", status=status.HTTP_201_CREATED)
            except Exception:
                return Response("Can't connect to IPStack", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Ip address missing", status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        if "ip_address" in request.data:
            obj = get_object_or_404(Localization, ip=request.data['ip_address'])
            serializer = LocalizationSerializer(obj, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Ip address missing", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if "ip_address" in request.data:
            obj = get_object_or_404(Localization, ip=request.data['ip_address'])
            obj.delete()
            return Response("Localization for ip_address: {} removed from the database".format(request.data['ip_address']), status=status.HTTP_200_OK)
        else:
            return Response("Ip address missing", status=status.HTTP_400_BAD_REQUEST)