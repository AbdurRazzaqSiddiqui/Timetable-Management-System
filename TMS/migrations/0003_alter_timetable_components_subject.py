# Generated by Django 5.0.4 on 2024-05-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TMS', '0002_timetable_components_delete_test_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable_components',
            name='subject',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]