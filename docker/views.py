from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DockerConfigSerializer


class DockerConfigView(APIView):
    def post(self, request):
        serializer = DockerConfigSerializer(data=request.data)

        if serializer.is_valid():
            docker_config = serializer.save()
            # command = docker_config.make_shell_command()
            print(docker_config)
            if docker_config.create_container_command():
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
