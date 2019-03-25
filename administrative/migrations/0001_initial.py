# Generated by Django 2.1.7 on 2019-03-25 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dpt', models.CharField(blank=True, default='', max_length=255)),
                ('pstn', models.CharField(blank=True, default='', max_length=255)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('level', models.IntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('bd_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administrative.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Teaching_Period',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('st_date', models.DateField()),
                ('en_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('credits', models.PositiveIntegerField()),
                ('image', models.CharField(default='default.jpg', max_length=255)),
                ('course_id', models.ManyToManyField(to='administrative.Course')),
            ],
        ),
    ]
