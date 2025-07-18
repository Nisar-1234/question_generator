# Generated by Django 5.2.4 on 2025-07-05 16:54

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskResult',
            fields=[
                ('task_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('progress', models.IntegerField(default=0)),
                ('result', models.JSONField(blank=True, default=dict)),
                ('error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='uploads/')),
                ('content', models.TextField()),
                ('detected_language', models.CharField(default='en', max_length=10)),
                ('word_count', models.IntegerField(default=0)),
                ('math_content_detected', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GeneratedQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('short_answer', 'Short Answer'), ('medium_answer', 'Medium Answer'), ('long_answer', 'Long Answer'), ('fill_blanks', 'Fill in the Blanks'), ('true_false', 'True/False'), ('matching', 'Matching')], max_length=20)),
                ('bloom_level', models.CharField(choices=[('remembering', 'Remembering'), ('understanding', 'Understanding'), ('applying', 'Applying'), ('analyzing', 'Analyzing'), ('evaluating', 'Evaluating'), ('creating', 'Creating')], max_length=20)),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], max_length=10)),
                ('answer', models.TextField(blank=True)),
                ('options', models.JSONField(blank=True, default=list)),
                ('explanation', models.TextField(blank=True)),
                ('topic', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.uploadedfile')),
            ],
            options={
                'ordering': ['bloom_level', 'question_type', 'created_at'],
            },
        ),
    ]
