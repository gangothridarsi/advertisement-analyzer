# Generated by Django 4.0.4 on 2022-05-25 17:17

import advapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('addId', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('adDescription', models.CharField(max_length=600)),
                ('adName', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to=advapp.models.path_and_rename)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email_id', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=20)),
                ('customer', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='UserResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emotion_name', models.CharField(max_length=20)),
                ('addId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advapp.advertisement')),
                ('username', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advapp.user')),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='advapp.user'),
        ),
    ]