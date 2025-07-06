# core/serializers.py
from rest_framework import serializers
from .models import UploadedFile, GeneratedQuestion, TaskResult
from rest_framework import serializers   # ✅ Correct

# Add this to your serializers.py:
from .models import (
    UploadedFile, GeneratedQuestion, TaskResult,
    BloomLevel, QuestionType, Difficulty, LLMProvider  # Add these
)
class UploadedFileSerializer(serializers.ModelSerializer):
    content_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedFile
        fields = ['id', 'filename', 'detected_language', 'word_count', 
                 'math_content_detected', 'content_preview', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_content_preview(self, obj):
        return obj.content[:500] + "..." if len(obj.content) > 500 else obj.content

class GeneratedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedQuestion
        fields = ['id', 'question_text', 'question_type', 'bloom_level', 
                 'difficulty', 'answer', 'options', 'explanation', 'topic', 'created_at']
        read_only_fields = ['id', 'created_at']

class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['task_id', 'status', 'progress', 'result', 'error', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class QuestionGenerationRequestSerializer(serializers.Serializer):
    file_id = serializers.UUIDField()
    bloom_levels = serializers.ListField(
        child=serializers.ChoiceField(choices=BloomLevel.choices),
        min_length=1
    )
    question_types = serializers.ListField(
        child=serializers.ChoiceField(choices=QuestionType.choices),
        min_length=1
    )
    difficulty = serializers.ChoiceField(choices=Difficulty.choices, default='medium')
    language = serializers.CharField(max_length=10, default='en')
    num_questions_per_type = serializers.IntegerField(min_value=1, max_value=20, default=5)
    llm_provider = serializers.ChoiceField(choices=LLMProvider.choices, default='openai')
    topic_focus = serializers.CharField(max_length=200, required=False)
