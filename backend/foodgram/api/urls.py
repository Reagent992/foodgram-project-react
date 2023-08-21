from django.urls import include, path
from rest_framework import routers

v1_router = routers.DefaultRouter()

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
