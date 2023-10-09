from rest_framework.serializers import ModelSerializer, JSONField
from .models import DockerConfigModel, DockerContainerModel


class DockerConfigSerializer(ModelSerializer):
    envs = JSONField()

    class Meta:
        model = DockerConfigModel
        fields = ("name", "image_address", "envs", "command")

    def create(self, validated_data):
        command = "docker create "
        envs = validated_data["envs"]
        for k, v in envs.items():
            command += f"-e {k}={v} "

        command += validated_data["image_address"]
        command += " "
        command += validated_data["command"]
        # TESTING HERE IN TERMINAL
        print(command)
        print("--------------------------------------------------------------")
        validated_data["command"] = command
        return super().create(validated_data)


class DockerContainerSerializer(ModelSerializer):
    class Meta:
        model = DockerContainerModel
        fields = "__all__"
