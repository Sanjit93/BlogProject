# Generated by Django 4.1.7 on 2023-08-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmedApp', '0002_alter_about_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='about_desc',
            field=models.TextField(max_length=300),
        ),
    ]