from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'url', views.TinyURLViewSet, basename='urls')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('v1/', include(router.urls)),
]
