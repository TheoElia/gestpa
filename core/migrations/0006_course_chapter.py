# Generated by Django 4.2.4 on 2024-11-10 16:53

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_account_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.CharField(default=core.models.generate_unique_id, editable=False, max_length=255, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('cover_image', models.ImageField(null=True, upload_to='courses')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.account')),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('uuid', models.CharField(default=core.models.generate_unique_id, editable=False, max_length=255, unique=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(null=True)),
                ('position', models.IntegerField(null=True)),
                ('cover_image', models.ImageField(null=True, upload_to='courses')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='core.course')),
            ],
            options={
                'db_table': 'chapter',
            },
        ),
    ]