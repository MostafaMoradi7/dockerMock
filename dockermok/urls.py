from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DockerContainerViewSet, ContainerHistoryViewSet

router = DefaultRouter()
router.register(r"apps", DockerContainerViewSet)
router.register(
    r"history", ContainerHistoryViewSet, basename="containerhistory"
)

urlpatterns = [
    path("", include(router.urls)),
]
