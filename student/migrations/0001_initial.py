# Generated by Django 2.1.7 on 2019-03-28 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrative', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lecturer', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=50)),
                ('tm_stmp', models.DateTimeField()),
                ('ip_addr', models.CharField(max_length=15)),
                ('q_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_class', models.ManyToManyField(to='lecturer.Class')),
                ('s_course', models.ManyToManyField(to='administrative.Course')),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.Student'),
        ),
        migrations.AddField(
            model_name='answer',
            name='teach_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Teaching_Day'),
        ),
    ]