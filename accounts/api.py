from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User

# Register API
class RegisterAPI(generics.GenericAPIView):
    """
    method: POST
    route: /api/auth/register
    summary: Used to register a user
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the post method for GenericAPIView
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(generics.GenericAPIView):
    """
    method: POST
    route: /api/auth/login
    summary: Used to log a user in
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Override the post method for the GenericAPIView
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    """
    method: GET
    route: /api/auth/user
    summary: Get the details for the current logged in user
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Get all Users API - needed to make a transaction to other user by username
class GetAllUsersAPI(generics.ListAPIView):
    """
    method: GET
    route: /api/auth/users
    summary: Get all the users on the platform
    """
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = UserSerializer
    queryset = User.objects.all()