# Generated by Django 2.1.5 on 2019-02-10 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mask', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='defectposition',
            unique_together={('mask', 'x', 'y')},
        ),
    ]