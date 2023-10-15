from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    DockerContainerSerializer,
    ContainerHistorySerializer,
    MessageSerializer,
)
from .models import DockerContainerModel, ContainerHistoryModel
import docker
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=DockerContainerSerializer,
    responses={status.HTTP_201_CREATED: DockerContainerSerializer},
)
class ContainerCreateView(APIView):
    def post(self, request, format=None):
        request.data["container_id"] = "temprary code here"
        serializer = DockerContainerSerializer(data=request.data)
        if serializer.is_valid():
            client = docker.from_env()
            try:
                data = serializer.validated_data
                new_container = client.containers.create(
                    name=data.get("name"),
                    image=data.get("image_address"),
                    environment=data.get("envs"),
                    command=data.get("command"),
                )
                serializer.validated_data["container_id"] = new_container.id
                serializer.save()

                ContainerHistoryModel.objects.create(
                    container=serializer.instance,
                    envs=data.get("envs"),
                    command=data.get("command"),
                )
                client.close()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(responses={status.HTTP_200_OK: DockerContainerSerializer(many=True)})
class ContainerListView(APIView):
    def get(self, request, format=None):
        containers = DockerContainerModel.objects.all()
        serializer = DockerContainerSerializer(containers, many=True)
        return Response(serializer.data)


@extend_schema(request=None, responses={status.HTTP_200_OK: DockerContainerSerializer})
class ContainerDetailView(APIView):
    def get(self, request, container_id, format=None):
        try:
            container = DockerContainerModel.objects.get(container_id=container_id)
            serializer = DockerContainerSerializer(container)
            return Response(serializer.data)
        except DockerContainerModel.DoesNotExist:
            return Response(
                {"error": "Container not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, container_id, format=None):
        try:
            container = DockerContainerModel.objects.get(container_id=container_id)
            client = docker.from_env()
            client.containers.get(container.container_id).remove(force=True)
            container.delete()
            client.close()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except DockerContainerModel.DoesNotExist:
            return Response(
                {"error": "Container not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@extend_schema(
    request=None,
    responses={
        status.HTTP_200_OK: MessageSerializer,
        status.HTTP_400_BAD_REQUEST: MessageSerializer,
    },
)
class ContainerStartView(APIView):
    def patch(self, request, container_id, format=None):
        try:
            container = DockerContainerModel.objects.get(container_id=container_id)
            client = docker.from_env()
            container_obj = client.containers.get(container.container_id)

            if container_obj.status != "running":
                container_obj.start()
                envs = container_obj.attrs["Config"]["Env"]
                command = container_obj.attrs["Config"]["Cmd"]

                ContainerHistoryModel.objects.create(
                    container=container,
                    status="STARTED",
                    envs=envs,
                    command=command,
                )
                client.close()
                return Response(
                    {"message": "Container started successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Container is not in a stopped state"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except DockerContainerModel.DoesNotExist:
            return Response(
                {"error": "Container not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


@extend_schema(
    responses={status.HTTP_200_OK: ContainerHistorySerializer(many=True)},
)
class ContainerHistoryRetrieveView(ReadOnlyModelViewSet):
    queryset = ContainerHistoryModel.objects.all()
    serializer_class = ContainerHistorySerializer
