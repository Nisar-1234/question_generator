from django.contrib import admin

# Register your models here.
# core/admin.py

from django.contrib import admin
from .models import UploadedFile, GeneratedQuestion, TaskResult
from django.contrib import admin


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'detected_language', 'word_count', 'math_content_detected', 'created_at']
    list_filter = ['detected_language', 'math_content_detected', 'created_at']
    search_fields = ['filename', 'content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('id', 'filename', 'file', 'user')
        }),
        ('Content Analysis', {
            'fields': ('detected_language', 'word_count', 'math_content_detected')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(GeneratedQuestion)
class GeneratedQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'bloom_level', 'question_type', 'difficulty', 'file', 'created_at']
    list_filter = ['bloom_level', 'question_type', 'difficulty', 'created_at']
    search_fields = ['question_text', 'answer', 'explanation']
    readonly_fields = ['id', 'created_at']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'

@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'status', 'progress', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['task_id', 'error']
    readonly_fields = ['task_id', 'created_at', 'updated_at']

