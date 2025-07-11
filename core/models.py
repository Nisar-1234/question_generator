# # # import os
# # # from pathlib import Path
# # # from decouple import config
# # # from django.db import models
# # # from django.contrib.auth.models import User
# # # import uuid
# # # from django.utils import timezone

# # # BASE_DIR = Path(__file__).resolve().parent.parent

# # # SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
# # # DEBUG = config('DEBUG', default=True, cast=bool)
# # # ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# # # # Application definition
# # # INSTALLED_APPS = [
# # #     'django.contrib.admin',
# # #     'django.contrib.auth',
# # #     'django.contrib.contenttypes',
# # #     'django.contrib.sessions',
# # #     'django.contrib.messages',
# # #     'django.contrib.staticfiles',
# # #     'rest_framework',
# # #     'corsheaders',
# # #     'channels',
# # #     'crispy_forms',
# # #     'crispy_bootstrap5',
# # #     'widget_tweaks',
# # #     'core',
# # # ]

# # # MIDDLEWARE = [
# # #     'django.middleware.security.SecurityMiddleware',
# # #     'whitenoise.middleware.WhiteNoiseMiddleware',
# # #     'corsheaders.middleware.CorsMiddleware',
# # #     'django.contrib.sessions.middleware.SessionMiddleware',
# # #     'django.middleware.common.CommonMiddleware',
# # #     'django.middleware.csrf.CsrfViewMiddleware',
# # #     'django.contrib.auth.middleware.AuthenticationMiddleware',
# # #     'django.contrib.messages.middleware.MessageMiddleware',
# # #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# # # ]

# # # ROOT_URLCONF = 'question_generator.urls'

# # # TEMPLATES = [
# # #     {
# # #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
# # #         'DIRS': [BASE_DIR / 'templates'],
# # #         'APP_DIRS': True,
# # #         'OPTIONS': {
# # #             'context_processors': [
# # #                 'django.template.context_processors.debug',
# # #                 'django.template.context_processors.request',
# # #                 'django.contrib.auth.context_processors.auth',
# # #                 'django.contrib.messages.context_processors.messages',
# # #             ],
# # #         },
# # #     },
# # # ]

# # # WSGI_APPLICATION = 'question_generator.wsgi.application'
# # # ASGI_APPLICATION = 'question_generator.asgi.application'

# # # # Database
# # # DATABASES = {
# # #     'default': {
# # #         'ENGINE': 'django.db.backends.sqlite3',
# # #         'NAME': BASE_DIR / 'db.sqlite3',
# # #     }
# # # }

# # # # Internationalization
# # # LANGUAGE_CODE = 'en-us'
# # # TIME_ZONE = 'UTC'
# # # USE_I18N = True
# # # USE_TZ = True

# # # # Static files
# # # STATIC_URL = '/static/'
# # # STATIC_ROOT = BASE_DIR / 'staticfiles'
# # # STATICFILES_DIRS = [BASE_DIR / 'static']

# # # # Media files
# # # MEDIA_URL = '/media/'
# # # MEDIA_ROOT = BASE_DIR / 'media'

# # # # Default primary key field type
# # # DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # # # REST Framework
# # # REST_FRAMEWORK = {
# # #     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# # #     'PAGE_SIZE': 20,
# # #     'DEFAULT_RENDERER_CLASSES': [
# # #         'rest_framework.renderers.JSONRenderer',
# # #     ],
# # #     'DEFAULT_PARSER_CLASSES': [
# # #         'rest_framework.parsers.JSONParser',
# # #         'rest_framework.parsers.MultiPartParser',
# # #     ],
# # # }

# # # # CORS
# # # CORS_ALLOWED_ORIGINS = [
# # #     "http://localhost:3000",
# # #     "http://127.0.0.1:3000",
# # # ]

# # # # Celery Configuration
# # # CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
# # # CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
# # # CELERY_ACCEPT_CONTENT = ['json']
# # # CELERY_TASK_SERIALIZER = 'json'
# # # CELERY_RESULT_SERIALIZER = 'json'

# # # # Channels
# # # CHANNEL_LAYERS = {
# # #     'default': {
# # #         'BACKEND': 'channels_redis.core.RedisChannelLayer',
# # #         'CONFIG': {
# # #             "hosts": [config('REDIS_URL', default='redis://localhost:6379/0')],
# # #         },
# # #     },
# # # }

# # # # Crispy Forms
# # # CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# # # CRISPY_TEMPLATE_PACK = "bootstrap5"

# # # # LLM API Keys
# # # OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
# # # ANTHROPIC_API_KEY = config('ANTHROPIC_API_KEY', default='')
# # # GEMINI_API_KEY = config('GEMINI_API_KEY', default='')


# # # core/models.py
# # from django.db import models
# # from django.contrib.auth.models import User
# # import uuid
# # from django.utils import timezone

# # class BloomLevel(models.TextChoices):
# #     REMEMBERING = 'remembering', 'Remembering'
# #     UNDERSTANDING = 'understanding', 'Understanding'
# #     APPLYING = 'applying', 'Applying'
# #     ANALYZING = 'analyzing', 'Analyzing'
# #     EVALUATING = 'evaluating', 'Evaluating'
# #     CREATING = 'creating', 'Creating'

# # class QuestionType(models.TextChoices):
# #     MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'
# #     SHORT_ANSWER = 'short_answer', 'Short Answer'
# #     MEDIUM_ANSWER = 'medium_answer', 'Medium Answer'
# #     LONG_ANSWER = 'long_answer', 'Long Answer'
# #     FILL_BLANKS = 'fill_blanks', 'Fill in the Blanks'
# #     TRUE_FALSE = 'true_false', 'True/False'
# #     MATCHING = 'matching', 'Matching'

# # class Difficulty(models.TextChoices):
# #     EASY = 'easy', 'Easy'
# #     MEDIUM = 'medium', 'Medium'
# #     HARD = 'hard', 'Hard'

# # class LLMProvider(models.TextChoices):
# #     OPENAI = 'openai', 'OpenAI'
# #     ANTHROPIC = 'anthropic', 'Anthropic'
# #     DEEPSEEK = 'deepseek', 'DeepSeek'
# #     GEMINI = 'gemini', 'Gemini'

# # class UploadedFile(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# #     filename = models.CharField(max_length=255)
# #     file = models.FileField(upload_to='uploads/')
# #     content = models.TextField()
# #     detected_language = models.CharField(max_length=10, default='en')
# #     word_count = models.IntegerField(default=0)
# #     math_content_detected = models.BooleanField(default=False)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         ordering = ['-created_at']

# #     def __str__(self):
# #         return f"{self.filename} ({self.word_count} words)"

# # class GeneratedQuestion(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='questions')
# #     question_text = models.TextField()
# #     question_type = models.CharField(max_length=20, choices=QuestionType.choices)
# #     bloom_level = models.CharField(max_length=20, choices=BloomLevel.choices)
# #     difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
# #     answer = models.TextField(blank=True)
# #     options = models.JSONField(default=list, blank=True)  # For multiple choice
# #     explanation = models.TextField(blank=True)
# #     topic = models.CharField(max_length=200, blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     class Meta:
# #         ordering = ['bloom_level', 'question_type', 'created_at']

# #     def __str__(self):
# #         return f"{self.get_bloom_level_display()} - {self.get_question_type_display()}"

# # class TaskResult(models.Model):
# #     TASK_STATUS = [
# #         ('pending', 'Pending'),
# #         ('processing', 'Processing'),
# #         ('completed', 'Completed'),
# #         ('failed', 'Failed'),
# #     ]
    
# #     task_id = models.CharField(max_length=255, unique=True, primary_key=True)
# #     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
# #     status = models.CharField(max_length=20, choices=TASK_STATUS, default='pending')
# #     progress = models.IntegerField(default=0)
# #     result = models.JSONField(default=dict, blank=True)
# #     error = models.TextField(blank=True)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# #     class Meta:
# #         ordering = ['-created_at']

# #     def __str__(self):
# #         return f"Task {self.task_id} - {self.status}"






# # core/models.py
# from django.db import models
# import uuid
# from django.utils import timezone

# class BloomLevel(models.TextChoices):
#     REMEMBERING = 'remembering', 'Remembering'
#     UNDERSTANDING = 'understanding', 'Understanding'
#     APPLYING = 'applying', 'Applying'
#     ANALYZING = 'analyzing', 'Analyzing'
#     EVALUATING = 'evaluating', 'Evaluating'
#     CREATING = 'creating', 'Creating'

# class QuestionType(models.TextChoices):
#     MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'
#     SHORT_ANSWER = 'short_answer', 'Short Answer'
#     MEDIUM_ANSWER = 'medium_answer', 'Medium Answer'
#     LONG_ANSWER = 'long_answer', 'Long Answer'
#     FILL_BLANKS = 'fill_blanks', 'Fill in the Blanks'
#     TRUE_FALSE = 'true_false', 'True/False'
#     MATCHING = 'matching', 'Matching'

# class Difficulty(models.TextChoices):
#     EASY = 'easy', 'Easy'
#     MEDIUM = 'medium', 'Medium'
#     HARD = 'hard', 'Hard'

# class LLMProvider(models.TextChoices):
#     OPENAI = 'openai', 'OpenAI'
#     ANTHROPIC = 'anthropic', 'Anthropic'
#     DEEPSEEK = 'deepseek', 'DeepSeek'
#     GEMINI = 'gemini', 'Gemini'

# class UploadedFile(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     filename = models.CharField(max_length=255)
#     file = models.FileField(upload_to='uploads/', null=True, blank=True)
#     content = models.TextField()
#     detected_language = models.CharField(max_length=10, default='en')
#     word_count = models.IntegerField(default=0)
#     math_content_detected = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.filename} ({self.word_count} words)"

# class GeneratedQuestion(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='questions')
#     question_text = models.TextField()
#     question_type = models.CharField(max_length=20, choices=QuestionType.choices)
#     bloom_level = models.CharField(max_length=20, choices=BloomLevel.choices)
#     difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
#     answer = models.TextField(blank=True)
#     options = models.JSONField(default=list, blank=True)
#     explanation = models.TextField(blank=True)
#     topic = models.CharField(max_length=200, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['bloom_level', 'question_type', 'created_at']

#     def __str__(self):
#         return f"{self.get_bloom_level_display()} - {self.get_question_type_display()}"

# class TaskResult(models.Model):
#     TASK_STATUS = [
#         ('pending', 'Pending'),
#         ('processing', 'Processing'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#     ]
    
#     task_id = models.CharField(max_length=255, unique=True, primary_key=True)
#     status = models.CharField(max_length=20, choices=TASK_STATUS, default='pending')
#     progress = models.IntegerField(default=0)
#     result = models.JSONField(default=dict, blank=True)
#     error = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Task {self.task_id} - {self.status}"


# from django.db import models
# import uuid
# from django.utils import timezone

# class Language(models.TextChoices):
#     ENGLISH = 'en', 'English'
#     HINDI = 'hi', 'Hindi (हिंदी)'
#     TELUGU = 'te', 'Telugu (తెలుగు)'
#     URDU = 'ur', 'Urdu (اردو)'
#     ARABIC = 'ar', 'Arabic (العربية)'
#     SPANISH = 'es', 'Spanish (Español)'
#     FRENCH = 'fr', 'French (Français)'
#     GERMAN = 'de', 'German (Deutsch)'
#     CHINESE = 'zh', 'Chinese (中文)'
#     JAPANESE = 'ja', 'Japanese (日本語)'
#     KOREAN = 'ko', 'Korean (한국어)'
#     RUSSIAN = 'ru', 'Russian (Русский)'
#     PORTUGUESE = 'pt', 'Portuguese (Português)'
#     ITALIAN = 'it', 'Italian (Italiano)'
#     BENGALI = 'bn', 'Bengali (বাংলা)'
#     TAMIL = 'ta', 'Tamil (தமிழ்)'
#     MALAYALAM = 'ml', 'Malayalam (മലയാളം)'
#     KANNADA = 'kn', 'Kannada (ಕನ್ನಡ)'
#     GUJARATI = 'gu', 'Gujarati (ગુજરાતી)'
#     MARATHI = 'mr', 'Marathi (मराठी)'
#     PUNJABI = 'pa', 'Punjabi (ਪੰਜਾਬੀ)'

# class ContentType(models.TextChoices):
#     TEXT = 'text', 'Text'
#     MATHEMATICAL = 'mathematical', 'Mathematical'
#     SCIENTIFIC = 'scientific', 'Scientific'
#     MIXED = 'mixed', 'Mixed Content'

# class MathematicalLevel(models.TextChoices):
#     BASIC = 'basic', 'Basic (Arithmetic)'
#     ALGEBRA = 'algebra', 'Algebra'
#     GEOMETRY = 'geometry', 'Geometry'
#     TRIGONOMETRY = 'trigonometry', 'Trigonometry'
#     CALCULUS = 'calculus', 'Calculus'
#     STATISTICS = 'statistics', 'Statistics'
#     DISCRETE = 'discrete', 'Discrete Math'
#     ADVANCED = 'advanced', 'Advanced Mathematics'

# class UploadedFile(models.Model):
    
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     filename = models.CharField(max_length=255)
#     file = models.FileField(upload_to='uploads/', null=True, blank=True)
#     content = models.TextField()
#     detected_language = models.CharField(max_length=10, default='en')
#     word_count = models.IntegerField(default=0)
#     math_content_detected = models.BooleanField(default=False)
    
#     # NEW FIELDS - Add these
#     content_type = models.CharField(max_length=20, default='text', blank=True)
#     mathematical_level = models.CharField(max_length=20, blank=True)
#     script_type = models.CharField(max_length=50, blank=True, default='latin')
#     reading_direction = models.CharField(max_length=3, default='ltr')
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# # class UploadedFile(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     filename = models.CharField(max_length=255)
# #     file = models.FileField(upload_to='uploads/', null=True, blank=True)
# #     content = models.TextField()
# #     detected_language = models.CharField(max_length=10, choices=Language.choices, default='en')
# #     word_count = models.IntegerField(default=0)
# #     math_content_detected = models.BooleanField(default=False)
# #     content_type = models.CharField(max_length=20, choices=ContentType.choices, default='text')
# #     mathematical_level = models.CharField(max_length=20, choices=MathematicalLevel.choices, blank=True)
    
# #     # Language-specific fields
# #     script_type = models.CharField(max_length=50, blank=True)  # devanagari, arabic, latin, etc.
# #     reading_direction = models.CharField(max_length=3, choices=[('ltr', 'Left to Right'), ('rtl', 'Right to Left')], default='ltr')
    
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

#     def get_font_family(self):
#         """Get appropriate font family for the language"""
#         script_fonts = {
#             'devanagari': 'Noto Sans Devanagari',
#             'telugu': 'Noto Sans Telugu',
#             'arabic': 'Noto Sans Arabic',
#             'chinese': 'Noto Sans CJK',
#             'default': 'Noto Sans'
#         }
#         return script_fonts.get(self.script_type, 'Noto Sans')

# class GeneratedQuestion(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='questions')
#     question_text = models.TextField()
#     question_text_formatted = models.TextField(blank=True)  # For LaTeX/MathML
#     question_type = models.CharField(max_length=20, choices=QuestionType.choices)
#     bloom_level = models.CharField(max_length=20, choices=BloomLevel.choices)
#     difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    
#     # Multi-language fields
#     language = models.CharField(max_length=10, choices=Language.choices, default='en')
    
#     # Mathematical fields
#     has_math = models.BooleanField(default=False)
#     math_expressions = models.JSONField(default=list, blank=True)  # Store LaTeX expressions
#     mathematical_level = models.CharField(max_length=20, choices=MathematicalLevel.choices, blank=True)
    
#     answer = models.TextField(blank=True)
#     answer_formatted = models.TextField(blank=True)  # For LaTeX/MathML answers
#     options = models.JSONField(default=list, blank=True)
#     options_formatted = models.JSONField(default=list, blank=True)  # For LaTeX options
#     explanation = models.TextField(blank=True)
#     explanation_formatted = models.TextField(blank=True)  # For LaTeX explanations
    
#     topic = models.CharField(max_length=200, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['bloom_level', 'question_type', 'created_at']











from django.db import models
import uuid
from django.utils import timezone

class BloomLevel(models.TextChoices):
    REMEMBERING = 'remembering', 'Remembering'
    UNDERSTANDING = 'understanding', 'Understanding'
    APPLYING = 'applying', 'Applying'
    ANALYZING = 'analyzing', 'Analyzing'
    EVALUATING = 'evaluating', 'Evaluating'
    CREATING = 'creating', 'Creating'

class QuestionType(models.TextChoices):
    MULTIPLE_CHOICE = 'multiple_choice', 'Multiple Choice'
    SHORT_ANSWER = 'short_answer', 'Short Answer'
    MEDIUM_ANSWER = 'medium_answer', 'Medium Answer'
    LONG_ANSWER = 'long_answer', 'Long Answer'
    FILL_BLANKS = 'fill_blanks', 'Fill in the Blanks'
    TRUE_FALSE = 'true_false', 'True/False'
    MATCHING = 'matching', 'Matching'

class Difficulty(models.TextChoices):
    EASY = 'easy', 'Easy'
    MEDIUM = 'medium', 'Medium'
    HARD = 'hard', 'Hard'

class LLMProvider(models.TextChoices):
    OPENAI = 'openai', 'OpenAI'
    ANTHROPIC = 'anthropic', 'Anthropic'
    DEEPSEEK = 'deepseek', 'DeepSeek'
    GEMINI = 'gemini', 'Gemini'

class Language(models.TextChoices):
    ENGLISH = 'en', 'English'
    HINDI = 'hi', 'Hindi (हिंदी)'
    TELUGU = 'te', 'Telugu (తెలుగు)'
    URDU = 'ur', 'Urdu (اردو)'
    ARABIC = 'ar', 'Arabic (العربية)'
    SPANISH = 'es', 'Spanish (Español)'
    FRENCH = 'fr', 'French (Français)'
    GERMAN = 'de', 'German (Deutsch)'
    CHINESE = 'zh', 'Chinese (中文)'
    JAPANESE = 'ja', 'Japanese (日本語)'
    KOREAN = 'ko', 'Korean (한국어)'
    RUSSIAN = 'ru', 'Russian (Русский)'
    PORTUGUESE = 'pt', 'Portuguese (Português)'
    ITALIAN = 'it', 'Italian (Italiano)'
    BENGALI = 'bn', 'Bengali (বাংলা)'
    TAMIL = 'ta', 'Tamil (தமிழ்)'
    MALAYALAM = 'ml', 'Malayalam (മലയാളം)'
    KANNADA = 'kn', 'Kannada (ಕನ್ನಡ)'
    GUJARATI = 'gu', 'Gujarati (ગુજરાતી)'
    MARATHI = 'mr', 'Marathi (मराठी)'
    PUNJABI = 'pa', 'Punjabi (ਪੰਜਾਬੀ)'

class ContentType(models.TextChoices):
    TEXT = 'text', 'Text'
    MATHEMATICAL = 'mathematical', 'Mathematical'
    SCIENTIFIC = 'scientific', 'Scientific'
    MIXED = 'mixed', 'Mixed Content'

class MathematicalLevel(models.TextChoices):
    BASIC = 'basic', 'Basic (Arithmetic)'
    ALGEBRA = 'algebra', 'Algebra'
    GEOMETRY = 'geometry', 'Geometry'
    TRIGONOMETRY = 'trigonometry', 'Trigonometry'
    CALCULUS = 'calculus', 'Calculus'
    STATISTICS = 'statistics', 'Statistics'
    DISCRETE = 'discrete', 'Discrete Math'
    ADVANCED = 'advanced', 'Advanced Mathematics'

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    content = models.TextField()
    detected_language = models.CharField(max_length=10, choices=Language.choices, default='en')
    word_count = models.IntegerField(default=0)
    math_content_detected = models.BooleanField(default=False)
    
    # Enhanced fields
    content_type = models.CharField(max_length=20, choices=ContentType.choices, default='text', blank=True)
    mathematical_level = models.CharField(max_length=20, choices=MathematicalLevel.choices, blank=True)
    script_type = models.CharField(max_length=50, blank=True, default='latin')
    reading_direction = models.CharField(max_length=3, choices=[('ltr', 'Left to Right'), ('rtl', 'Right to Left')], default='ltr')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename} ({self.word_count} words)"

    def get_font_family(self):
        """Get appropriate font family for the language"""
        script_fonts = {
            'devanagari': 'Noto Sans Devanagari',
            'telugu': 'Noto Sans Telugu',
            'arabic': 'Noto Sans Arabic',
            'chinese': 'Noto Sans CJK',
            'default': 'Noto Sans'
        }
        return script_fonts.get(self.script_type, 'Noto Sans')

class GeneratedQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_text_formatted = models.TextField(blank=True)  # For LaTeX/MathML
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    bloom_level = models.CharField(max_length=20, choices=BloomLevel.choices)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    
    # Multi-language fields
    language = models.CharField(max_length=10, choices=Language.choices, default='en')
    
    # Mathematical fields
    has_math = models.BooleanField(default=False)
    math_expressions = models.JSONField(default=list, blank=True)  # Store LaTeX expressions
    mathematical_level = models.CharField(max_length=20, choices=MathematicalLevel.choices, blank=True)
    
    answer = models.TextField(blank=True)
    answer_formatted = models.TextField(blank=True)  # For LaTeX/MathML answers
    options = models.JSONField(default=list, blank=True)
    options_formatted = models.JSONField(default=list, blank=True)  # For LaTeX options
    explanation = models.TextField(blank=True)
    explanation_formatted = models.TextField(blank=True)  # For LaTeX explanations
    
    topic = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['bloom_level', 'question_type', 'created_at']

    def __str__(self):
        return f"{self.get_bloom_level_display()} - {self.get_question_type_display()}"

class TaskResult(models.Model):
    TASK_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True, primary_key=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='pending')
    progress = models.IntegerField(default=0)
    result = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"