"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_rest.views import (
    SignUpView,
    ProjectViewSet,
    ContributorsViewSet,
    IssuesViewSet,
    CommentsViewSet
)

from swagger.views import (
    DecoratedTokenVerifyView,
    DecoratedTokenRefreshView,
    DecoratedTokenObtainPairView,
    DecoratedTokenBlacklistView
)

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register(r'^projects/(?P<project_id>[0-9]+)/users', ContributorsViewSet, basename='users')
router.register(r'^projects/(?P<project_id>[0-9]+)/issues', IssuesViewSet, basename='issues')
router.register(r'^projects/(?P<project_id>[0-9]+)/issues/(?P<issue_id>[0-9]+)/comments', CommentsViewSet,
                basename='comments')

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # EndPoint with router
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # Swagger for docs
    # This exposes 4 endpoints:
    # A JSON view of your API specification at /swagger.json
    # A YAML view of your API specification at /swagger.yaml
    # A swagger-ui view of your API specification at /swagger/
    # A ReDoc view of your API specification at /redoc/
    path('accounts/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # EndPoints for Login and SignUp
    path('login', DecoratedTokenObtainPairView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    # simplejwt urls and views for the Swagger
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', DecoratedTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', DecoratedTokenVerifyView.as_view(), name='token_verify'),
    path('api/token/black_list/', DecoratedTokenBlacklistView.as_view(), name='token_black_list')
]
