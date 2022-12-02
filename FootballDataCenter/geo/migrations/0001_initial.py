# Generated by Django 3.2 on 2022-11-26 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=64)),
                ('code_alpha_3', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('code_alpha_2', models.CharField(max_length=3)),
                ('region', models.CharField(max_length=16, null=True)),
                ('sub_region', models.CharField(max_length=64, null=True)),
            ],
        ),
    ]
