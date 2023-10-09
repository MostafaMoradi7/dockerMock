from django.db import models

import subprocess


class DockerConfigModel(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=100)
    image_address = models.CharField(max_length=200)
    command = models.CharField(max_length=300)
    envs = models.JSONField()

    def create_container_command(self):
        try:
            subprocess.check_call(self.command)

            return True
        except subprocess.CalledProcessError:
            return False
