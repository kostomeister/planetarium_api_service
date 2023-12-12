from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import (
    PlanetariumDome,
    ShowTheme,
    AstronomyShow,
    ShowSession,
    Reservation
)
from .serializers import (
    PlanetariumDomeSerializer,
    ShowThemeSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer,
    ShowSessionSerializer,
    ShowSessionDetailSerializer,
    ShowSessionListSerializer,
    ReservationSerializer,
    ReservationListSerializer
)
from .permissions import IsAdminOrIfAuthenticatedReadOnly


class PlanetariumDomeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class ShowThemeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("show_theme")
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        title = self.request.query_params.get("title")
        show_themes = self.request.query_params.get("show_theme")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if show_themes:
            show_themes_ids = self._params_to_ints(show_themes)
            queryset = queryset.filter(show_theme__id__in=show_themes_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowDetailSerializer

        return AstronomyShowSerializer

    # only for documentation
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_themes",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by show theme id(ex. ?show_theme=3,5)"
            ),
            OpenApiParameter(
                "title",
                type=str,
                description="Filter by title (ex. ?title=AstronomyShow Title)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )

    def get_queryset(self):
        date = self.request.query_params.get("title")
        astronomy_show = self.request.query_params.get("show_theme")
        planetarium_dome = self.request.query_params.get("planetarium_dome")

        queryset = self.queryset

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if astronomy_show:
            queryset = queryset.filter(astronomy_show__id=astronomy_show)

        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__id=planetarium_dome)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer

        if self.action == "retrieve":
            return ShowSessionDetailSerializer

        return ShowSessionSerializer

    # only for documentation
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date",
                type=datetime,
                description="Filter by date(ex. ?date=2012-11-03)"
            ),
            OpenApiParameter(
                "astronomy_show",
                type=int,
                description="Filter by astronomy show id (ex. ?astronomy_show=1)",
            ),
            OpenApiParameter(
                "planetarium_dome",
                type=int,
                description="Filter by planetarium dome id (ex. ?planetarium_dome=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related("tickets")
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
