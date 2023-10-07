from django.db import models

# Create your models here.


class DockerConfigModel(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    envs = models.JSONField()
    command = models.CharField(max_length=300)
