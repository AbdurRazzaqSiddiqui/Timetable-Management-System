# Generated by Django 5.0.4 on 2024-05-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TMS', '0010_subject_credit_hrs'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]