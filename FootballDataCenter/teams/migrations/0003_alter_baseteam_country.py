# Generated by Django 4.1 on 2023-03-29 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0001_initial'),
        ('teams', '0002_remove_baseteam_date_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseteam',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.country'),
        ),
    ]
