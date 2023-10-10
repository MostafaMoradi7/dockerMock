from django.db import models


class DockerContainerModel(models.Model):
    container_id = models.CharField(primary_key=True, max_length=150)
    name = models.CharField(max_length=100)
    image_address = models.CharField(max_length=200)
    command = models.CharField(max_length=300)
    envs = models.JSONField()

    def __str__(self) -> str:
        return super().__str__()


class ContainerHistoryModel(models.Model):
    STATUS_CHOICES = (
        ("RUNNING", "running"),
        ("FINISHED", "finished"),
        ("CREATED", "created"),
    )
    container = models.ForeignKey(
        "DockerContainerModel", on_delete=models.CASCADE
    )
    envs = models.JSONField()
    command = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    action_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="CREATED"
    )


class MessageModel(models.Model):
    message = models.CharField(max_length=200)
