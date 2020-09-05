from rest_framework import routers
from .api import WalletCreateAPI, WalletUpdateAPI, WalletDetailsAPI
from django.urls import path

urlpatterns = [
    path('api/wallet/create', WalletCreateAPI.as_view()),
    path('api/wallet/<int:pk>', WalletUpdateAPI.as_view()),
    path('api/wallet', WalletDetailsAPI.as_view()),
]