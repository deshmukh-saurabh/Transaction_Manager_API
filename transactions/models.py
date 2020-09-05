from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    owner = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE, null=True)
    reciever = models.ForeignKey(User, related_name='transactions_reciever', on_delete=models.CASCADE, null=True)
    reciever_username = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=500, blank=True)
    amount = models.IntegerField()
    performed_at = models.DateTimeField(auto_now_add=True)