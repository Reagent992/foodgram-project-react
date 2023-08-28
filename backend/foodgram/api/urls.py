from django.urls import include, path
from rest_framework import routers

from api.views import (RecipesViewSet, TagViewSet,
                       IngredientsViewSet, FavoriteViewSet)

v1_router = routers.DefaultRouter()
v1_router.register(r"recipes/(?P<recipe_id>\d+)/favorite",
                   FavoriteViewSet)
v1_router.register("recipes", RecipesViewSet)
v1_router.register("tags", TagViewSet)
v1_router.register("ingredients", IngredientsViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
