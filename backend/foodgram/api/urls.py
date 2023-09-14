from django.urls import include, path
from rest_framework import routers

from api.views.ingredients import IngredientsViewSet
from api.views.recipes import RecipesViewSet
from api.views.subscriptions import UserViewSet
from api.views.tags import TagViewSet

v1_router = routers.DefaultRouter()
v1_router.register('recipes',
                   RecipesViewSet, basename='recipes')
v1_router.register('tags',
                   TagViewSet)
v1_router.register('ingredients',
                   IngredientsViewSet)
v1_router.register('users',
                   UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
