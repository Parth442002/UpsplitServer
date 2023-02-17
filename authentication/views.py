from os import stat
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, permissions


from .models import Account
from .serializers import MyTokenObtainPairSerializer, ProfileSerializer
from django.contrib.auth import get_user_model

user_model = get_user_model()


class AccountLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class AccountLogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            rtoken = request.data["refresh_token"]
            refresh_token = RefreshToken(rtoken)

            atoken = request.data["access_token"]
            access_token = AccessToken(atoken)

            refresh_token.blacklist()
            access_token.blacklist()

            return Response(
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        x = user_model.objects.get(id=request.user.id)
        serializer = ProfileSerializer(x,)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
