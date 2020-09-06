from .models import Wallet
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import WalletSerializer

class WalletCreateAPI(generics.CreateAPIView):
    """
    method: POST
    route: /api/wallet/create
    summary: Used to Create a Wallet for the current logged in user
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer

    def post(self, request, *args, **kwargs):
        """
        Overrides the post method for CreateAPIView
        """

        queryset = Wallet.objects.all()

        # check if user already has a wallet created (one wallet per user)
        if len(queryset) != 0:
            query = queryset.filter(owner=self.request.user)
            if query: # user already has a wallet
                return Response({
                    "message": "User already has a wallet!"
                })

        # else create a wallet
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = serializer.save(owner=self.request.user)
        return Response({
            "wallet": WalletSerializer(wallet, context=self.get_serializer_context()).data
        })

class WalletUpdateAPI(generics.UpdateAPIView):
    """
    method: PUT
    route: /api/wallet/<wallet_id>
    summary: Used to update wallet balance (add money)
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()


class WalletDetailsAPI(generics.ListAPIView):
    """
    method: GET
    route: /api/wallet
    summary: Get the wallet details for the logged in user
    """

    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer
    
    def get_queryset(self):
        return Wallet.objects.filter(owner=self.request.user)