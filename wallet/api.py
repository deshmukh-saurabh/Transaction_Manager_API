from .models import Wallet
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import WalletSerializer

class WalletCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer

    def post(self, request, *args, **kwargs):
        queryset = Wallet.objects.all()
        if len(queryset) != 0:
            query = queryset.filter(owner=self.request.user)
            if query: # user already has a wallet
                return Response({
                    "message": "User already has a wallet!"
                })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = serializer.save(owner=self.request.user)
        return Response({
            "wallet": WalletSerializer(wallet, context=self.get_serializer_context()).data
        })

class WalletUpdateAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()


class WalletDetailsAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = WalletSerializer
    
    def get_queryset(self):
        return Wallet.objects.filter(owner=self.request.user)