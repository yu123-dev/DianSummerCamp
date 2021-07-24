# Generated by Django 3.1.7 on 2021-07-22 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Tea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('details', models.TextField()),
                ('status', models.IntegerField(default=1)),
                ('picture', models.CharField(max_length=100)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mytea.store')),
            ],
        ),
    ]
