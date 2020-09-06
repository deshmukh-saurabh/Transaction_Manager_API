from django.contrib.auth.models import User
from .models import Transaction
from wallet.models import Wallet
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import TransactionSerializer
from django.core.exceptions import ObjectDoesNotExist

class TransactionCreateAPI(generics.CreateAPIView):
    """
    method: POST
    route: /api/transactions/
    summary: Used for performing a transaction for a logged in user.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TransactionSerializer

    def perform_updates(self):
        """
        summary: Method used to perform updates to wallet while performing a transaction.

        Returns:
            True: if update was successful
            False: if update not possible
        """
        curr_data = self.request.data
        owner = self.request.user
        reciever_id = User.objects.get(username=curr_data['reciever_username']).id
        value = int(curr_data['amount'])

        # Update(Decrease) sender's balance
        wallet = Wallet.objects.get(owner=owner)
        curr_balance = wallet.balance
        updated_balance = curr_balance - value
        if(updated_balance < 0): # insufficient balance
            return False
        
        wallet.balance = updated_balance
        wallet.save()

        # Update(Increase) reciever's balance
        wallet = Wallet.objects.get(owner=reciever_id)
        curr_balance = wallet.balance
        wallet.balance = curr_balance + value
        wallet.save()

        return True

    def is_wallet_created(self):
        """
        Method to check if the current logged in user has a wallet

        Returns:
            True: if the current logged in user has a wallet created
            False: otherwise
        """
        try:
            Wallet.objects.get(owner=self.request.user)
        except Wallet.DoesNotExist:
            return False
        
        return True
        

    def post(self, request, *args, **kwargs):
        """
        Method used to override post method for the CreateAPIView
        """

        # Check if wallet is created
        if not self.is_wallet_created():
            return Response({
                "message": "Wallet not created!"
            })

        # Check if we can perform the transaction
        if not self.perform_updates():
            return Response({
                "message": "Insufficient balance!"
            })

        # if the code got here, perform the transaction
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(owner=self.request.user, reciever=User.objects.get(username=request.data['reciever_username']))
        return Response({
            "transaction": TransactionSerializer(transaction, context=self.get_serializer_context()).data
        })

class TransactionDetailsAPI(generics.ListAPIView):
    """
    method: GET
    route:/api/transactions/all
    summary: Used to view all the transaction history for the current logged in user
    Returns: All the transactions(sent/recieved) for the current user
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user) | Transaction.objects.filter(reciever=self.request.user)