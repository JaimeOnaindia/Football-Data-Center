# Generated by Django 3.2 on 2022-11-26 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date_birth', models.DateField(null=True)),
                ('team_name', models.CharField(max_length=30)),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.country')),
            ],
        ),
    ]
