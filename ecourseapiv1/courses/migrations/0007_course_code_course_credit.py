# Generated by Django 4.2.13 on 2024-05-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_image_lesson_image_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='code',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name='course',
            name='credit',
            field=models.CharField(default=0, max_length=1),
        ),
    ]
