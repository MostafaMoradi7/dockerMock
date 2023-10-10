from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContainerDetailView,
    ContainerCreateView,
    ContainerListView,
    ContainerStopView,
    ContainerStartView,
    ContainerLogsView,
    ContainerHistoryRetrieveView,
)

router = DefaultRouter()
router.register(r"history", ContainerHistoryRetrieveView)


urlpatterns = [
    path("", include(router.urls)),
    path("apps/", ContainerCreateView.as_view(), name="container-create"),
    path("apps/list/", ContainerListView.as_view(), name="container-list"),
    path(
        "apps/<str:container_id>/",
        ContainerDetailView.as_view(),
        name="container-detail",
    ),
    path(
        "apps/<str:container_id>/stop/",
        ContainerStopView.as_view(),
        name="container-stop",
    ),
    path(
        "apps/<str:container_id>/start/",
        ContainerStartView.as_view(),
        name="container-start",
    ),
    path(
        "apps/<str:container_id>/logs/",
        ContainerLogsView.as_view(),
        name="container-logs",
    ),
]
