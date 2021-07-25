from django.conf import settings
from django.urls import path
from .views import LocalizationView

urlpatterns = [
    path('', LocalizationView.as_view(), name='ipstack-localization'),
]
