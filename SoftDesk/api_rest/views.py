from django.http import QueryDict
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings

from api_rest.permissions import IsResponsableAuthenticated

from api_rest.serializers import (
    SignUpSerializer,
    ProjetsSerializer,
    ContributorsSerializer,
    ContributorsListSerializer,
)

from api_rest.models import Users, Projects, Contributors


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows project where user is attached, to be viewed or edited, or created a new one.
    """
    serializer_class = ProjetsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_anonymous:
            queryset = Projects.objects.filter(contributors = self.request.user)
        if self.request.user.is_superuser:
            queryset = Projects.objects.all()
        return queryset


class ContributorsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows 'responsable' to add, view, and delete contributors to a project.
    """
    serializer_class = ContributorsSerializer
    list_serializer_class = ContributorsListSerializer
    permission_classes = [IsResponsableAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()
    
    def get_queryset(self):
        """
        :return: Contributors in project_id  in url
        """
        project_id = self.kwargs['project_id']
        queryset = Contributors.objects.filter(project = project_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Add item 'projet' in serializer.data from url
        :param request:
        :param args:
        :param kwargs: project_id in url
        :return: response created status
        """
        project_id = self.kwargs['project_id']
        body = QueryDict(mutable = True)
        print(request.data)
        for key, value in request.data.items():
            body.__setitem__(key, value)
        body.__setitem__('project', project_id)
        body._mutable = False
        print(body)
        serializer = self.get_serializer(data = body)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class SignUpView(generics.CreateAPIView):
    """
    API endpoint that allows an user to be created.
    """
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

# queryset = Projects.object.all().order_by('-date_joined')
