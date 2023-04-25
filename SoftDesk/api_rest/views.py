from django.contrib.auth.models import Group
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from api_rest.serializers import SignUpSerializer
from api_rest.models import Users


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Users.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]


class SignUpView(generics.CreateAPIView):
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer
