from django.urls import path, include
from rest_framework import routers

from planetarium.views import PlanetariumDomeViewSet

router = routers.DefaultRouter()

router.register("planetarium_dome", PlanetariumDomeViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium"
