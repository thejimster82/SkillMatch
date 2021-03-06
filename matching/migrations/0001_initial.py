# Generated by Django 2.1.5 on 2019-04-24 14:51

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
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MatchesTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matching_sent', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matching_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major', models.CharField(blank=True, max_length=100)),
                ('grad_year', models.IntegerField(default=0)),
                ('bio', models.TextField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('first_login', models.BooleanField(default=True)),
                ('profilePicture', models.ImageField(blank=True, upload_to='images')),
                ('rank', models.IntegerField(default=0)),
                ('tutor', models.BooleanField(default=False)),
                ('tutor_bio', models.TextField(blank=True, default='')),
                ('tutor_gpa', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True)),
                ('courses', models.ManyToManyField(blank=True, to='matching.Course')),
                ('matches', models.ManyToManyField(blank=True, related_name='matching', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
