from rest_framework import routers
from .api import TransactionCreateAPI, TransactionDetailsAPI
from django.urls import path

urlpatterns = [
    path('api/transactions/', TransactionCreateAPI.as_view()),
    path('api/transactions/all', TransactionDetailsAPI.as_view()),
]