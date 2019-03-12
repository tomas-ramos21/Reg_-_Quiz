# Generated by Django 2.1.7 on 2019-03-09 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=50)),
                ('tm_stmp', models.DateTimeField()),
                ('ip_t', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.CharField(max_length=9, primary_key=True, serialize=False)),
                ('time_commi', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('school', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('sha', models.CharField(max_length=255)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=40)),
                ('dpt', models.CharField(max_length=30)),
                ('pstn', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('ans_1', models.TextField()),
                ('ans_2', models.TextField()),
                ('ans_3', models.TextField()),
                ('ans_4', models.TextField()),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('code', models.PositiveIntegerField()),
                ('level', models.IntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('bd_code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('sha', models.CharField(max_length=255)),
                ('f_name', models.CharField(max_length=50)),
                ('l_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('s_class', models.ManyToManyField(to='lecturer.Class')),
                ('s_course', models.ManyToManyField(to='lecturer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teaching_Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('st_time', models.DateTimeField()),
                ('en_time', models.DateTimeField()),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Class')),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Teaching_Period',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('st_date', models.DateField()),
                ('en_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('code', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('credits', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Unit'),
        ),
        migrations.AddField(
            model_name='class',
            name='course_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Course'),
        ),
        migrations.AddField(
            model_name='class',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Employee'),
        ),
        migrations.AddField(
            model_name='class',
            name='t_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Teaching_Period'),
        ),
        migrations.AddField(
            model_name='class',
            name='unit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Unit'),
        ),
        migrations.AddField(
            model_name='answer',
            name='q_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='s_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Student'),
        ),
        migrations.AddField(
            model_name='answer',
            name='teach_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lecturer.Teaching_Day'),
        ),
    ]
