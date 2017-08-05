from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import SignInSerializer, SelfDataSerializer, UserSerializer
from .permissions import IsSelfOrReadOnly


class SignInView(APIView):

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = data['user']
        Token.objects.get_or_create(user=user)
        serializer = SelfDataSerializer(instance=user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class AccountsViewSet(ListModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, IsSelfOrReadOnly)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            return User.objects.all()
        return User.objects.filter(department=user.department)
