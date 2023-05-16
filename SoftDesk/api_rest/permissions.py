from rest_framework.permissions import BasePermission
from api_rest.models import Contributors


class IsAuthorAuthenticated(BasePermission):
    message = 'Customers have not the role of author on this project or authenticated.'

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs responsable du projets et authentifiés
        is_author = False
        project_id = request.parser_context['kwargs'].get('project_id')
        if_contributor = Contributors.objects.filter(user=request.user, project=project_id)
        if if_contributor.exists():
            contributor = Contributors.objects.get(user=request.user, project=project_id)
            if contributor.role == "Auteur":
                is_author = True
        return bool(request.user and request.user.is_authenticated and is_author)


class IsJustContributorsAuthenticated(BasePermission):
    message = 'Customers is not a Contributors of this project or authenticated.'

    def has_object_permission(self, request, view, obj):
        # Ne donnons l’accès qu’aux utilisateurs contributors du projets et authentifiés
        is_contributor = False
        if_contributor = Contributors.objects.filter(user=request.user, project=obj.pk)
        if if_contributor.exists():
            is_contributor = True
        return bool(request.user and request.user.is_authenticated and is_contributor)


class ContributorOrAuthorPermissions(BasePermission):
    """
    Contributor have permission to have List a detail, but only author (or assignee for Issues) can "write" or delete
    """
    # message = 'Customers is not the author or for PUT or PATCH method it may be assignee.'

    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs contributors du projets et authentifiés pour GET List or CREATE
        is_contributor = False
        project_id = request.parser_context['kwargs'].get('project_id')
        if_contributor = Contributors.objects.filter(user=request.user, project=project_id)
        if if_contributor.exists():
            is_contributor = True
        return bool(request.user and request.user.is_authenticated and is_contributor)

    def has_object_permission(self, request, view, obj):
        # DELETE method just the author not assignee for Issues,
        # GET Detail for contributors others method only author
        project_id = request.parser_context['kwargs'].get('project_id')
        if_contributor = Contributors.objects.filter(user=request.user, project=project_id)
        if request.method == "PUT" or request.method == "PATCH":
            if view.__class__.__name__ == "IssuesViewSet":
                if request.user == obj.author or request.user == obj.assignee:
                    if if_contributor.exists():
                        return True
        if view.__class__.__name__ == "CommentsViewSet":
            if request.method == "GET":
                if if_contributor.exists():
                    return True
        return bool(request.user and request.user.is_authenticated and if_contributor.exists()
                    and (request.user == obj.author))
