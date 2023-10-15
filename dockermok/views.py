from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import (
    DockerContainerSerializer,
    ContainerHistorySerializer,
    MessageSerializer,
)
from .models import DockerContainerModel, ContainerHistoryModel
import docker
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404


class DockerContainerViewSet(viewsets.ModelViewSet):
    serializer_class = DockerContainerSerializer
    queryset = DockerContainerModel.objects.all()

    @extend_schema(
        responses={status.HTTP_200_OK: DockerContainerSerializer(many=True)}
    )
    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=DockerContainerSerializer,
        responses={status.HTTP_201_CREATED: DockerContainerSerializer},
    )
    def create(self, request):
        request.data["container_id"] = "temporary code here"
        serializer = self.get_serializer(data=request.data)
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

    @extend_schema(
        request=None, responses={status.HTTP_200_OK: DockerContainerSerializer}
    )
    def retrieve(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(container)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: MessageSerializer,
            status.HTTP_400_BAD_REQUEST: MessageSerializer,
        },
    )
    def partial_update(self, request, pk=None):
        container = get_object_or_404(self.queryset, pk=pk)
        client = docker.from_env()
        container_obj = client.containers.get(container.container_id)
        print("---------------------------------------------------")
        try:
            if container_obj.status != "running":
                print("I am NOT running")
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
                print("I am Running!")
                container_obj.stop()
                envs = container_obj.attrs["Config"]["Env"]
                command = container_obj.attrs["Config"]["Cmd"]

                ContainerHistoryModel.objects.create(
                    container=container,
                    status="FINISHED",
                    envs=envs,
                    command=command,
                )
                client.close()
                return Response(
                    {"message": "Container Stoped successfully"},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        request=DockerContainerSerializer,
        responses={status.HTTP_200_OK: DockerContainerSerializer},
    )
    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )

            if serializer.is_valid():
                client = docker.from_env()
                data = serializer.validated_data
                container = client.containers.get(instance.container_id)

                instance.name = data["name"]
                instance.envs = data["envs"]
                instance.command = data["command"]
                instance.image_address = data["image_address"]
                container.stop()

                new_container = client.containers.create(
                    name=instance.name,
                    image=instance.image_address,
                    environment=instance.envs,
                    command=instance.command,
                )

                prev_container_id = instance.container_id
                instance.container_id = new_container.id
                container.remove()
                if not instance.command.startswith("docker"):
                    command = serializer.create_command_for_docker(data)
                    instance.command = command

                instance.save()

                DockerContainerModel.objects.filter(
                    container_id=prev_container_id
                ).delete()

                historys = ContainerHistoryModel.objects.filter(
                    container__container_id=None
                ).update(container=instance)

                client.close()
                ContainerHistoryModel.objects.create(
                    container=instance,
                    envs=data["envs"],
                    command=instance.command,
                    description="Modified containing container to another!",
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        request=None, responses={status.HTTP_204_NO_CONTENT: "No Content"}
    )
    def destroy(self, request, pk=None):
        try:
            container = get_object_or_404(self.queryset, pk=pk)
            client = docker.from_env()
            client.containers.get(container.name).remove(force=True)
            container.delete()
            client.close()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            ContainerHistoryModel.objects.filter(
                container__isnull=True
            ).delete()


class ContainerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerHistorySerializer
    queryset = ContainerHistoryModel.objects.all()
