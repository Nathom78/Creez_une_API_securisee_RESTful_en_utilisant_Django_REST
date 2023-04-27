from rest_framework.permissions import BasePermission
from api_rest.models import Contributors, Issues


class IsResponsableAuthenticated(BasePermission):
    message = 'Customers is not a Responsable of this project or authenticated.'
    
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs responsable du projets et authentifiés
        is_responsable = False
        project_id = request.parser_context['kwargs'].get('project_id')
        print(request.user)
        
        contributor = Contributors.objects.filter(user = request.user, project = project_id)
        if contributor:
            if contributor.role == "Responsable":
                is_responsable = True
        
        return bool(request.user and request.user.is_authenticated and is_responsable)


class IsContributorsAuthenticated(BasePermission):
    message = 'Customers is not a Contributors of this project or authenticated.'
    
    def has_permission(self, request, view):
        # Ne donnons l’accès qu’aux utilisateurs contributors du projets et authentifiés
        is_responsable = False
        project_id = request.parser_context['kwargs'].get('project_id')
        contributor = Contributors.objects.get(user = request.user, project = project_id)
        
        return bool(request.user and request.user.is_authenticated and is_responsable)
