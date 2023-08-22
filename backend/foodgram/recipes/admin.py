from django.contrib import admin

from recipes.models import (Tag, Recipe, Ingredients, Subscription,
                            FavoriteRecipe, MeasurementUnit, ShoppingCart)

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredients)
admin.site.register(Subscription)
admin.site.register(FavoriteRecipe)
admin.site.register(MeasurementUnit)
admin.site.register(ShoppingCart)
