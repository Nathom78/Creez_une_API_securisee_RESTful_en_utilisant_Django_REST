from django.http import QueryDict
from rest_framework import viewsets, generics, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


from api_rest.permissions import (
    IsResponsableAuthenticated,
    ContributorOrAuthorPermissions,
    IsJustContributorsAuthenticated
)
from api_rest.serializers import (
    SignUpSerializer,
    ProjetSerializer,
    ProjetsListSerializer,
    ContributorSerializer,
    ContributorsListSerializer,
    IssueSerializer,
    IssueListSerializer,
    CommentSerializer,
    CommentListSerializer
)

from api_rest.models import Users, Projects, Contributors, Issues, Comments


def body_insertion(self, request):
    """
    Add in request.data before to serialized and validate.
    Add item 'projet' in serializer.data from url (if not exist...)
    For IssuesView Add item 'assignee' in serializer.data if not exist
    For CommentView add item 'issue' from url (if not exist ...)
    :param self:
    :param request:
    :return: body
    """
    view = self.__class__.__name__
    project_id = self.kwargs['project_id']
    body = QueryDict(mutable = True)
    # intercept request.data for make body
    for key, value in request.data.items():
        body.__setitem__(key, value)
    # Look for variable is in request.data and put this from Url.
    project = body.get("project", default = None)

    if view == "IssuesViewSet":
        assignee = body.get("assignee", default = None)
        author = body.get("author", default = None)
        if assignee is None and author is not None:
            if request.method != "PATCH":
                body.__setitem__('assignee', author)
    if view != "CommentsViewSet":
        if project is None:
            body.__setitem__('project', project_id)
    if view == "CommentsViewSet":
        issue = body.get("project", default = None)
        issue_id = self.kwargs['issue_id']
        user_id = request.user.id
        author = body.get("author", default = None)
        if issue is None:
            body.__setitem__('issue', issue_id)
        if author is None:
            body.__setitem__('author', user_id)
    body._mutable = False
    return body


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows project where user is attached, to be listed, viewed, edited, deleted, or created a new
    one.
    """
    serializer_class = ProjetSerializer
    list_serializer_class = ProjetsListSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsJustContributorsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_anonymous:
            queryset = Projects.objects.filter(contributors = self.request.user)
        if self.request.user.is_superuser:
            queryset = Projects.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        
        serializer = self.get_serializer(data = request.data)
        print(serializer)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        
        # Save the user like a contributor responsable for this project
        project_id = serializer.data["id"]
        responsable_model = {"user": request.user.id, "project": project_id, "role": "Responsable"}
        user_serializer = ContributorSerializer(data = responsable_model)
        user_serializer.is_valid(raise_exception = True)
        user_serializer.save()
        # Update the instance created with Contributors updated
        serializer_instance = Projects.objects.get(pk = project_id)
        serializer = self.get_serializer(serializer_instance)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class ContributorsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    """
    API endpoint that allows 'responsable' to add, view, and delete contributors to a project.
    """
    serializer_class = ContributorSerializer
    list_serializer_class = ContributorsListSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsResponsableAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        """
        :return: Contributors in project_id  in url
        """
        queryset = self.queryset
        if self.kwargs:
            project_id = self.kwargs['project_id']
            queryset = Contributors.objects.filter(project = project_id)
        return queryset

    def create(self, request, *args, **kwargs):

        body = body_insertion(self, request)

        serializer = self.get_serializer(data = body)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class IssuesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin):
    """
        API endpoint that allows Issues from a project where user is attached, to be listed, deleted, edited,
        or created a new one.
    """
    serializer_class = IssueSerializer
    list_serializer_class = IssueListSerializer
    permission_classes = [ContributorOrAuthorPermissions]

    def get_queryset(self):
        """
        :return: Issues in project_id in url
        """
        queryset = self.queryset
        if self.kwargs:
            project_id = self.kwargs['project_id']
            queryset = Issues.objects.filter(project = project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        body = body_insertion(self, request)

        serializer = self.get_serializer(data = body)

        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        body = body_insertion(self, request)

        serializer = self.get_serializer(instance, data = body, partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()


class CommentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comment to an issue from a project where user is attached, to be listed, viewed, deleted,
    edited, or created a new one.
    """
    serializer_class = CommentSerializer
    list_serializer_class = CommentListSerializer
    permission_classes = [ContributorOrAuthorPermissions]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def get_queryset(self):
        """
        :return: Comments from an issue in url
        """
        queryset = self.queryset
        if self.kwargs:
            issue_id = self.kwargs['issue_id']
            queryset = Comments.objects.filter(issue = issue_id)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):

        body = body_insertion(self, request)

        serializer = self.get_serializer(data = body)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        body = body_insertion(self, request)

        serializer = self.get_serializer(instance, data = body, partial = partial)
        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """ Exemple for add in the header the last-updated_time of this comment, for avoid to save
            But for List view we can add the last comment updated with time
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        dict_serializer = serializer.data
        headers = {"last_updated": dict_serializer["created_time"]}
        return Response(serializer.data, headers = headers)


class SignUpView(generics.CreateAPIView):
    """
    API endpoint that allows an user to be created.
    """
    queryset = Users.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

# queryset = Projects.object.all().order_by('-date_joined')
