from django.urls import include, path
from rest_framework import routers

from api.views import (RecipesViewSet, TagViewSet,
                       IngredientsViewSet, FavoriteViewSet,
                       ListCreateDestoySubscriptionViewSet,
                       ShoppingCartViewSet)

v1_router = routers.DefaultRouter()
v1_router.register("recipes",
                   RecipesViewSet)
v1_router.register(r"recipes/(?P<recipe_id>\d+)/favorite",
                   FavoriteViewSet)
v1_router.register(r"recipes/(?P<recipe_id>\d+)/shopping_cart",
                   ShoppingCartViewSet)
v1_router.register("tags",
                   TagViewSet)
v1_router.register("ingredients",
                   IngredientsViewSet)
v1_router.register("users/subscriptions",
                   ListCreateDestoySubscriptionViewSet,
                   basename='subscriptions')
v1_router.register(r"users/(?P<target_user>\d+)/subscribe",
                   ListCreateDestoySubscriptionViewSet,
                   basename='subscriptions')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
