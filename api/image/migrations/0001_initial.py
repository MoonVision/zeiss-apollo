# Generated by Django 2.1.5 on 2019-02-10 01:08

from django.db import migrations, models
import django.utils.timezone
import image.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(height_field='height', upload_to=image.models.image_path, width_field='width')),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
        ),
    ]
