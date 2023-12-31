# Generated by Django 4.2.6 on 2023-10-15 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DockerContainerModel",
            fields=[
                (
                    "container_id",
                    models.CharField(
                        max_length=150, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("image_address", models.CharField(max_length=200)),
                ("command", models.CharField(max_length=300)),
                ("envs", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="MessageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="ContainerHistoryModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("envs", models.JSONField()),
                ("command", models.CharField(max_length=300)),
                ("description", models.TextField(blank=True, null=True)),
                ("action_date", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RUNNING", "running"),
                            ("FINISHED", "finished"),
                            ("CREATED", "created"),
                        ],
                        default="CREATED",
                        max_length=10,
                    ),
                ),
                (
                    "container",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dockermok.dockercontainermodel",
                    ),
                ),
            ],
        ),
    ]
