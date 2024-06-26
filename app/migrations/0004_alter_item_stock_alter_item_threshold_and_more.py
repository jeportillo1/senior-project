# Generated by Django 4.0 on 2022-05-12 05:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='threshold',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='recent_new_user',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
