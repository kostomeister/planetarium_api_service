from django.urls import path, include
from rest_framework import routers

from planetarium.views import PlanetariumDomeViewSet, ShowThemeViewSet

router = routers.DefaultRouter()

router.register("planetarium_dome", PlanetariumDomeViewSet)
router.register("show_theme", ShowThemeViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium"
