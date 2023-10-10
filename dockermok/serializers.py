from rest_framework.serializers import ModelSerializer, JSONField
from .models import DockerContainerModel, ContainerHistoryModel, MessageModel


class DockerContainerSerializer(ModelSerializer):
    envs = JSONField()

    class Meta:
        model = DockerContainerModel
        fields = ("container_id", "name", "image_address", "envs", "command")

    def _create_command_for_docker(self, validated_data):
        command = "docker create "
        envs = validated_data["envs"]
        for k, v in envs.items():
            command += f"-e {k}={v} "

        if (
            not validated_data["name"] == ""
            or not validated_data["name"] is None
        ):
            command += f"--name={validated_data['name']} "

        command += validated_data["image_address"]
        command += " "
        command += validated_data["command"]
        return command

    def create(self, validated_data):
        validated_data["command"] = self._create_command_for_docker(
            validated_data=validated_data
        )
        return super().create(validated_data)


class ContainerHistorySerializer(ModelSerializer):
    class Meta:
        model = ContainerHistoryModel
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ("message",)
