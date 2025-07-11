# # # # # core/tasks.py
# # # # from celery import shared_task
# # # # from django.utils import timezone
# # # # from .models import TaskResult, GeneratedQuestion, UploadedFile
# # # # from .llm_providers import LLMProviderFactory
# # # # import json

# # # # @shared_task(bind=True)
# # # # def generate_questions_task(self, file_id: str, request_data: dict):
# # # #     task_id = self.request.id
    
# # # #     try:
# # # #         # Get file
# # # #         file_obj = UploadedFile.objects.get(id=file_id)
        
# # # #         # Create or update task result
# # # #         task_result, created = TaskResult.objects.get_or_create(
# # # #             task_id=task_id,
# # # #             defaults={
# # # #                 'status': 'processing',
# # # #                 'progress': 10,
# # # #                 'created_at': timezone.now(),
# # # #                 'updated_at': timezone.now()
# # # #             }
# # # #         )
        
# # # #         # Initialize LLM provider
# # # #         provider = LLMProviderFactory.create_provider(request_data["llm_provider"])
        
# # # #         # Update progress
# # # #         task_result.progress = 30
# # # #         task_result.save()
        
# # # #         # Generate questions
# # # #         questions = provider.generate_questions(file_obj.content, request_data)
        
# # # #         # Update progress
# # # #         task_result.progress = 70
# # # #         task_result.save()
        
# # # #         # Save questions to database
# # # #         for question_data in questions:
# # # #             GeneratedQuestion.objects.create(
# # # #                 file=file_obj,
# # # #                 question_text=question_data["question_text"],
# # # #                 question_type=question_data["question_type"],
# # # #                 bloom_level=question_data["bloom_level"],
# # # #                 difficulty=question_data["difficulty"],
# # # #                 answer=question_data["answer"],
# # # #                 options=question_data["options"],
# # # #                 explanation=question_data["explanation"]
# # # #             )
        
# # # #         # Complete task
# # # #         task_result.status = 'completed'
# # # #         task_result.progress = 100
# # # #         task_result.result = {"questions": questions, "count": len(questions)}
# # # #         task_result.updated_at = timezone.now()
# # # #         task_result.save()
        
# # # #         return {"status": "completed", "questions": questions}
        
# # # #     except Exception as e:
# # # #         # Handle error
# # # #         task_result.status = 'failed'
# # # #         task_result.error = str(e)
# # # #         task_result.updated_at = timezone.now()
# # # #         task_result.save()
        
# # # #         return {"status": "failed", "error": str(e)}




# # # # core/tasks.py
# # # from celery import shared_task
# # # from django.utils import timezone
# # # from .models import TaskResult, GeneratedQuestion, UploadedFile
# # # from .llm_providers import LLMProviderFactory
# # # import json

# # # @shared_task(bind=True)
# # # def generate_questions_task(self, file_id: str, request_data: dict):
# # #     """Background task to generate questions"""
# # #     task_id = self.request.id
    
# # #     try:
# # #         # Get file
# # #         file_obj = UploadedFile.objects.get(id=file_id)
        
# # #         # Create or update task result
# # #         task_result, created = TaskResult.objects.get_or_create(
# # #             task_id=task_id,
# # #             defaults={
# # #                 'status': 'processing',
# # #                 'progress': 10,
# # #                 'created_at': timezone.now(),
# # #                 'updated_at': timezone.now()
# # #             }
# # #         )
        
# # #         # Update progress
# # #         task_result.progress = 30
# # #         task_result.save()
        
# # #         # Initialize LLM provider
# # #         provider = LLMProviderFactory.create_provider(request_data.get("llm_provider", "openai"))
        
# # #         # Update progress
# # #         task_result.progress = 50
# # #         task_result.save()
        
# # #         # Generate questions
# # #         questions = provider.generate_questions(file_obj.content, request_data)
        
# # #         # Update progress
# # #         task_result.progress = 80
# # #         task_result.save()
        
# # #         # Save questions to database
# # #         question_count = 0
# # #         for question_data in questions:
# # #             GeneratedQuestion.objects.create(
# # #                 file=file_obj,
# # #                 question_text=question_data["question_text"],
# # #                 question_type=question_data["question_type"],
# # #                 bloom_level=question_data["bloom_level"],
# # #                 difficulty=question_data["difficulty"],
# # #                 answer=question_data.get("answer", ""),
# # #                 options=question_data.get("options", []),
# # #                 explanation=question_data.get("explanation", "")
# # #             )
# # #             question_count += 1
        
# # #         # Complete task
# # #         task_result.status = 'completed'
# # #         task_result.progress = 100
# # #         task_result.result = {"questions": question_count, "file_id": file_id}
# # #         task_result.updated_at = timezone.now()
# # #         task_result.save()
        
# # #         return {"status": "completed", "questions": question_count}
        
# # #     except Exception as e:
# # #         # Handle error
# # #         error_msg = str(e)
# # #         try:
# # #             task_result.status = 'failed'
# # #             task_result.error = error_msg
# # #             task_result.updated_at = timezone.now()
# # #             task_result.save()
# # #         except:
# # #             pass  # If task_result doesn't exist, that's ok
        
# # #         return {"status": "failed", "error": error_msg}

# # # @shared_task
# # # def test_task():
# # #     """Simple test task"""
# # #     return "Hello from Celery - working correctly!"









# # # core/tasks.py
# # from celery import shared_task
# # from django.utils import timezone
# # from .models import TaskResult, GeneratedQuestion, UploadedFile
# # from .llm_providers import LLMProviderFactory
# # import json

# # @shared_task(bind=True)
# # def generate_questions_task(self, file_id: str, request_data: dict):
# #     """Generate questions in background - now using mock provider"""
# #     task_id = self.request.id
    
# #     try:
# #         # Get the uploaded file
# #         try:
# #             file_obj = UploadedFile.objects.get(id=file_id)
# #         except UploadedFile.DoesNotExist:
# #             return {"status": "failed", "error": f"File with id {file_id} not found"}
        
# #         # Create task result record
# #         task_result, created = TaskResult.objects.get_or_create(
# #             task_id=task_id,
# #             defaults={
# #                 'status': 'processing',
# #                 'progress': 10,
# #                 'created_at': timezone.now(),
# #                 'updated_at': timezone.now()
# #             }
# #         )
        
# #         # Update progress
# #         task_result.progress = 30
# #         task_result.save()
        
# #         # Get the provider (now always MockProvider)
# #         provider = LLMProviderFactory.create_provider(request_data.get("llm_provider", "openai"))
        
# #         # Update progress
# #         task_result.progress = 50
# #         task_result.save()
        
# #         # Generate questions using mock provider
# #         questions = provider.generate_questions(file_obj.content, request_data)
        
# #         # Update progress
# #         task_result.progress = 70
# #         task_result.save()
        
# #         # Save questions to database
# #         saved_count = 0
# #         for question_data in questions:
# #             try:
# #                 GeneratedQuestion.objects.create(
# #                     file=file_obj,
# #                     question_text=question_data["question_text"],
# #                     question_type=question_data["question_type"],
# #                     bloom_level=question_data["bloom_level"],
# #                     difficulty=question_data["difficulty"],
# #                     answer=question_data.get("answer", ""),
# #                     options=question_data.get("options", []),
# #                     explanation=question_data.get("explanation", "")
# #                 )
# #                 saved_count += 1
# #             except Exception as e:
# #                 print(f"Error saving question: {e}")
# #                 continue
        
# #         # Complete the task
# #         task_result.status = 'completed'
# #         task_result.progress = 100
# #         task_result.result = {"questions": saved_count, "file_id": file_id}
# #         task_result.updated_at = timezone.now()
# #         task_result.save()
        
# #         return {"status": "completed", "questions": saved_count}
        
# #     except Exception as e:
# #         # Handle any errors
# #         error_msg = str(e)
# #         print(f"Task failed with error: {error_msg}")
        
# #         try:
# #             # Update task result with error
# #             task_result = TaskResult.objects.get(task_id=task_id)
# #             task_result.status = 'failed'
# #             task_result.error = error_msg
# #             task_result.updated_at = timezone.now()
# #             task_result.save()
# #         except:
# #             pass
        
# #         return {"status": "failed", "error": error_msg}

# # @shared_task
# # def test_celery():
# #     """Simple test task to verify Celery is working"""
# #     return "Celery is working correctly!"

# # @shared_task(bind=True)
# # def generate_questions_task_enhanced(self, file_id: str, request_data: dict):
# #     """Enhanced task with multi-language and math support"""
# #     task_id = self.request.id
    
# #     try:
# #         from .models import TaskResult, GeneratedQuestion, UploadedFile
# #         from .multilingual_generator import EnhancedLLMProviderFactory
        
# #         file_obj = UploadedFile.objects.get(id=file_id)
        
# #         task_result, created = TaskResult.objects.get_or_create(
# #             task_id=task_id,
# #             defaults={'status': 'processing', 'progress': 10}
# #         )
        
# #         # Enhanced provider with language support
# #         language = request_data.get('language', file_obj.detected_language)
# #         provider = EnhancedLLMProviderFactory.create_provider('enhanced', language)
        
# #         task_result.progress = 50
# #         task_result.save()
        
# #         # Add content type and mathematical level to request
# #         request_data['content_type'] = file_obj.content_type
# #         request_data['mathematical_level'] = file_obj.mathematical_level
        
# #         # Generate enhanced questions
# #         questions = provider.generate_questions(file_obj.content, request_data)
        
# #         task_result.progress = 80
# #         task_result.save()
        
# #         count = 0
# #         for question_data in questions:
# #             GeneratedQuestion.objects.create(
# #                 file=file_obj,
# #                 question_text=question_data["question_text"],
# #                 question_text_formatted=question_data.get("question_text_formatted", ""),
# #                 question_type=question_data["question_type"],
# #                 bloom_level=question_data["bloom_level"],
# #                 difficulty=question_data["difficulty"],
# #                 language=question_data.get("language", language),
# #                 has_math=question_data.get("has_math", False),
# #                 math_expressions=question_data.get("math_expressions", []),
# #                 mathematical_level=question_data.get("mathematical_level", ""),
# #                 answer=question_data.get("answer", ""),
# #                 answer_formatted=question_data.get("answer_formatted", ""),
# #                 options=question_data.get("options", []),
# #                 options_formatted=question_data.get("options_formatted", []),
# #                 explanation=question_data.get("explanation", ""),
# #                 explanation_formatted=question_data.get("explanation_formatted", "")
# #             )
# #             count += 1
        
# #         task_result.status = 'completed'
# #         task_result.progress = 100
# #         task_result.result = {"questions": count, "file_id": file_id}
# #         task_result.save()
        
# #         return {"status": "completed", "questions": count}
        
# #     except Exception as e:
# #         return {"status": "failed", "error": str(e)}
# # # Update the task in core/tasks.py
# # @shared_task(bind=True)
# # def generate_questions_task(self, file_id: str, request_data: dict):
# #     """Generate questions in the same language as the uploaded file"""
# #     task_id = self.request.id
    
# #     try:
# #         from .models import TaskResult, GeneratedQuestion, UploadedFile
# #         from .language_question_generator import LanguageSpecificQuestionGenerator
        
# #         # Get file
# #         file_obj = UploadedFile.objects.get(id=file_id)
        
# #         # Create task result
# #         task_result, created = TaskResult.objects.get_or_create(
# #             task_id=task_id,
# #             defaults={'status': 'processing', 'progress': 10}
# #         )
        
# #         # IMPORTANT: Use the detected language from the file
# #         detected_language = file_obj.detected_language
        
# #         # Create language-specific generator
# #         generator = LanguageSpecificQuestionGenerator(language=detected_language)
        
# #         task_result.progress = 30
# #         task_result.save()
        
# #         # Get request parameters
# #         bloom_levels = request_data.get("bloom_levels", ["remembering"])
# #         question_types = request_data.get("question_types", ["multiple_choice"])
# #         difficulty = request_data.get("difficulty", "medium")
# #         num_questions = request_data.get("num_questions_per_type", 2)
        
# #         task_result.progress = 50
# #         task_result.save()
        
# #         # Generate questions in the detected language
# #         count = 0
# #         question_number = 1
        
# #         for bloom_level in bloom_levels:
# #             for question_type in question_types:
# #                 for i in range(num_questions):
# #                     # Generate question in the same language as the file
# #                     question_data = generator.generate_question(
# #                         content=file_obj.content,
# #                         bloom_level=bloom_level,
# #                         question_type=question_type,
# #                         difficulty=difficulty,
# #                         question_number=question_number
# #                     )
                    
# #                     # Save to database
# #                     GeneratedQuestion.objects.create(
# #                         file=file_obj,
# #                         question_text=question_data["question_text"],
# #                         question_type=question_data["question_type"],
# #                         bloom_level=question_data["bloom_level"],
# #                         difficulty=question_data["difficulty"],
# #                         language=detected_language,  # Set to detected language
# #                         has_math=question_data["has_math"],
# #                         math_expressions=question_data["math_expressions"],
# #                         mathematical_level=question_data["mathematical_level"],
# #                         answer=question_data["answer"],
# #                         options=question_data["options"],
# #                         explanation=question_data["explanation"]
# #                     )
                    
# #                     count += 1
# #                     question_number += 1
        
# #         task_result.status = 'completed'
# #         task_result.progress = 100
# #         task_result.result = {"questions": count, "file_id": file_id, "language": detected_language}
# #         task_result.save()
        
# #         return {"status": "completed", "questions": count, "language": detected_language}
        
# #     except Exception as e:
# #         return {"status": "failed", "error": str(e)}







# # core/tasks.py
# from celery import shared_task
# from django.utils import timezone
# from .models import TaskResult, GeneratedQuestion, UploadedFile
# import json

# @shared_task
# def test_celery():
#     """Simple test task to verify Celery is working"""
#     return "Celery is working correctly!"

# @shared_task(bind=True)
# def generate_questions_task(self, file_id: str, request_data: dict):
#     """
#     Main task to generate questions with multilingual and mathematical support.
#     Uses enhanced generator when available, falls back to basic generation.
#     """
#     task_id = self.request.id
    
#     try:
#         from .models import TaskResult, GeneratedQuestion, UploadedFile
        
#         # Get the uploaded file
#         try:
#             file_obj = UploadedFile.objects.get(id=file_id)
#         except UploadedFile.DoesNotExist:
#             return {"status": "failed", "error": f"File with id {file_id} not found"}
        
#         # Create task result record
#         task_result, created = TaskResult.objects.get_or_create(
#             task_id=task_id,
#             defaults={
#                 'status': 'processing',
#                 'progress': 10,
#                 'created_at': timezone.now(),
#                 'updated_at': timezone.now()
#             }
#         )
        
#         # Get detected language from file
#         detected_language = getattr(file_obj, 'detected_language', 'en')
        
#         # Update progress
#         task_result.progress = 30
#         task_result.save()
        
#         # Try to use enhanced multilingual generator first
#         try:
#             from .multilingual_generator import EnhancedLLMProviderFactory
#             use_enhanced = True
#         except ImportError:
#             try:
#                 from .language_question_generator import LanguageSpecificQuestionGenerator
#                 use_language_specific = True
#                 use_enhanced = False
#             except ImportError:
#                 use_enhanced = False
#                 use_language_specific = False
        
#         # Update progress
#         task_result.progress = 50
#         task_result.save()
        
#         # Extract request parameters
#         bloom_levels = request_data.get("bloom_levels", ["remembering"])
#         question_types = request_data.get("question_types", ["multiple_choice"])
#         difficulty = request_data.get("difficulty", "medium")
#         num_questions = request_data.get("num_questions_per_type", 2)
        
#         # Update progress
#         task_result.progress = 70
#         task_result.save()
        
#         count = 0
#         questions = []
        
#         if use_enhanced:
#             # Use enhanced multilingual generator with math support
#             try:
#                 language = request_data.get('language', detected_language)
#                 provider = EnhancedLLMProviderFactory.create_provider('enhanced', language)
                
#                 # Add content type and mathematical level to request
#                 enhanced_request_data = request_data.copy()
#                 enhanced_request_data['content_type'] = getattr(file_obj, 'content_type', 'text')
#                 enhanced_request_data['mathematical_level'] = getattr(file_obj, 'mathematical_level', 'basic')
#                 enhanced_request_data['language'] = language
                
#                 # Generate enhanced questions
#                 questions = provider.generate_questions(file_obj.content, enhanced_request_data)
                
#             except Exception as e:
#                 print(f"Enhanced generator failed: {e}, falling back to basic generation")
#                 use_enhanced = False
        
#         if not use_enhanced and use_language_specific:
#             # Use language-specific generator
#             try:
#                 generator = LanguageSpecificQuestionGenerator(language=detected_language)
#                 question_number = 1
                
#                 for bloom_level in bloom_levels:
#                     for question_type in question_types:
#                         for i in range(num_questions):
#                             question_data = generator.generate_question(
#                                 content=file_obj.content,
#                                 bloom_level=bloom_level,
#                                 question_type=question_type,
#                                 difficulty=difficulty,
#                                 question_number=question_number
#                             )
#                             questions.append(question_data)
#                             question_number += 1
                            
#             except Exception as e:
#                 print(f"Language-specific generator failed: {e}, falling back to basic generation")
#                 use_language_specific = False
        
#         if not use_enhanced and not use_language_specific:
#             # Fallback to basic question generation
#             question_number = 1
#             for bloom_level in bloom_levels:
#                 for question_type in question_types:
#                     for i in range(num_questions):
#                         # Generate basic questions based on language
#                         if detected_language == 'hi':
#                             question_text = f"प्रश्न {question_number}: इस दस्तावेज़ में मुख्य अवधारणाएं क्या हैं?"
#                             answer = "यह एक नमूना उत्तर है"
#                             options = ["विकल्प A", "विकल्प B", "विकल्प C", "विकल्प D"] if question_type == "multiple_choice" else []
#                         elif detected_language == 'te':
#                             question_text = f"ప్రశ్న {question_number}: ఈ పత్రంలోని ప్రధాన భావనలు ఏమిటి?"
#                             answer = "ఇది ఒక నమూనా సమాధానం"
#                             options = ["ఎంపిక A", "ఎంపిక B", "ఎంపిక C", "ఎంపిక D"] if question_type == "multiple_choice" else []
#                         elif detected_language == 'ur':
#                             question_text = f"سوال {question_number}: اس دستاویز میں اہم تصورات کیا ہیں؟"
#                             answer = "یہ ایک نمونہ جواب ہے"
#                             options = ["آپشن A", "آپشن B", "آپشن C", "آپشن D"] if question_type == "multiple_choice" else []
#                         else:
#                             question_text = f"Question {question_number}: What are the main concepts in this document?"
#                             answer = "This is a sample answer"
#                             options = ["Option A", "Option B", "Option C", "Option D"] if question_type == "multiple_choice" else []
                        
#                         question_data = {
#                             "question_text": question_text,
#                             "question_text_formatted": question_text,
#                             "question_type": question_type,
#                             "bloom_level": bloom_level,
#                             "difficulty": difficulty,
#                             "language": detected_language,
#                             "has_math": False,
#                             "mathematical_level": "",
#                             "math_expressions": [],
#                             "answer": answer,
#                             "answer_formatted": answer,
#                             "options": options,
#                             "options_formatted": options,
#                             "explanation": f"Generated question for {bloom_level} level",
#                             "explanation_formatted": f"Generated question for {bloom_level} level"
#                         }
#                         questions.append(question_data)
#                         question_number += 1
        
#         # Save questions to database
#         for question_data in questions:
#             try:
#                 # Create question with all available fields
#                 question_obj = GeneratedQuestion.objects.create(
#                     file=file_obj,
#                     question_text=question_data["question_text"],
#                     question_type=question_data["question_type"],
#                     bloom_level=question_data["bloom_level"],
#                     difficulty=question_data["difficulty"],
#                     answer=question_data.get("answer", ""),
#                     options=question_data.get("options", []),
#                     explanation=question_data.get("explanation", "")
#                 )
                
#                 # Set additional fields if they exist in the model
#                 if hasattr(question_obj, 'question_text_formatted'):
#                     question_obj.question_text_formatted = question_data.get("question_text_formatted", "")
#                 if hasattr(question_obj, 'language'):
#                     question_obj.language = question_data.get("language", detected_language)
#                 if hasattr(question_obj, 'has_math'):
#                     question_obj.has_math = question_data.get("has_math", False)
#                 if hasattr(question_obj, 'math_expressions'):
#                     question_obj.math_expressions = question_data.get("math_expressions", [])
#                 if hasattr(question_obj, 'mathematical_level'):
#                     question_obj.mathematical_level = question_data.get("mathematical_level", "")
#                 if hasattr(question_obj, 'answer_formatted'):
#                     question_obj.answer_formatted = question_data.get("answer_formatted", "")
#                 if hasattr(question_obj, 'options_formatted'):
#                     question_obj.options_formatted = question_data.get("options_formatted", [])
#                 if hasattr(question_obj, 'explanation_formatted'):
#                     question_obj.explanation_formatted = question_data.get("explanation_formatted", "")
                
#                 question_obj.save()
#                 count += 1
                
#             except Exception as e:
#                 print(f"Error saving question: {e}")
#                 continue
        
#         # Complete the task
#         task_result.status = 'completed'
#         task_result.progress = 100
#         task_result.result = {
#             "questions": count, 
#             "file_id": file_id, 
#             "language": detected_language,
#             "generator_used": "enhanced" if use_enhanced else ("language_specific" if use_language_specific else "basic")
#         }
#         task_result.updated_at = timezone.now()
#         task_result.save()
        
#         return {
#             "status": "completed", 
#             "questions": count, 
#             "language": detected_language,
#             "generator_used": "enhanced" if use_enhanced else ("language_specific" if use_language_specific else "basic")
#         }
        
#     except Exception as e:
#         # Handle any errors
#         error_msg = str(e)
#         print(f"Task failed with error: {error_msg}")
        
#         try:
#             # Update task result with error
#             task_result = TaskResult.objects.get(task_id=task_id)
#             task_result.status = 'failed'
#             task_result.error = error_msg
#             task_result.updated_at = timezone.now()
#             task_result.save()
#         except Exception as save_error:
#             print(f"Error saving task failure: {save_error}")
        
#         return {"status": "failed", "error": error_msg}

# @shared_task(bind=True)
# def generate_questions_task_enhanced(self, file_id: str, request_data: dict):
#     """
#     Legacy enhanced task - redirects to main task
#     This is kept for backward compatibility
#     """
#     return generate_questions_task(self, file_id, request_data)





# core/tasks.py - Updated version with better AI integration
from celery import shared_task
from django.utils import timezone
from .models import TaskResult, GeneratedQuestion, UploadedFile
import json
import logging

logger = logging.getLogger(__name__)

@shared_task
def test_celery():
    """Simple test task to verify Celery is working"""
    return "Celery is working correctly!"

@shared_task(bind=True)
def generate_questions_task(self, file_id: str, request_data: dict):
    """
    Enhanced task to generate questions with real AI integration
    """
    task_id = self.request.id
    
    try:
        from .models import TaskResult, GeneratedQuestion, UploadedFile
        from .llm_providers import LLMProviderFactory
        
        logger.info(f"Starting question generation for file {file_id}")
        logger.info(f"Request params: {request_data}")
        
        # Get the uploaded file
        try:
            file_obj = UploadedFile.objects.get(id=file_id)
            logger.info(f"File found: {file_obj.filename}, content length: {len(file_obj.content)}")
        except UploadedFile.DoesNotExist:
            error_msg = f"File with id {file_id} not found"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
        
        # Create task result record
        task_result, created = TaskResult.objects.get_or_create(
            task_id=task_id,
            defaults={
                'status': 'processing',
                'progress': 10,
                'created_at': timezone.now(),
                'updated_at': timezone.now()
            }
        )
        
        # Get detected language from file
        detected_language = getattr(file_obj, 'detected_language', 'en')
        logger.info(f"Detected language: {detected_language}")
        
        # Update progress
        task_result.progress = 30
        task_result.save()
        
        # Get the LLM provider (now with real AI)
        provider = LLMProviderFactory.create_provider(request_data.get("llm_provider", "openai"))
        logger.info(f"Provider created: {type(provider).__name__}")
        
        # Update progress
        task_result.progress = 50
        task_result.save()
        
        # Extract request parameters with validation
        bloom_levels = request_data.get("bloom_levels", ["remembering"])
        question_types = request_data.get("question_types", ["multiple_choice"])
        difficulty = request_data.get("difficulty", "medium")
        num_questions = request_data.get("num_questions_per_type", 2)
        language = request_data.get("language", detected_language)
        
        # Validate parameters
        if not bloom_levels or not question_types:
            error_msg = "Invalid parameters: bloom_levels and question_types are required"
            logger.error(error_msg)
            task_result.status = 'failed'
            task_result.error = error_msg
            task_result.save()
            return {"status": "failed", "error": error_msg}
        
        logger.info(f"Generating questions with params: bloom_levels={bloom_levels}, types={question_types}, difficulty={difficulty}")
        
        # Enhanced request data for AI
        enhanced_request_data = {
            'bloom_levels': bloom_levels,
            'question_types': question_types,
            'difficulty': difficulty,
            'num_questions_per_type': num_questions,
            'language': language,
            'llm_provider': request_data.get("llm_provider", "openai"),
            'topic_focus': request_data.get('topic_focus', ''),
        }
        
        # Update progress
        task_result.progress = 70
        task_result.save()
        
        # Generate questions using AI provider
        logger.info("Calling AI provider to generate questions...")
        questions = provider.generate_questions(file_obj.content, enhanced_request_data)
        logger.info(f"Generated {len(questions)} questions")
        
        if not questions:
            error_msg = "No questions were generated"
            logger.error(error_msg)
            task_result.status = 'failed'
            task_result.error = error_msg
            task_result.save()
            return {"status": "failed", "error": error_msg}
        
        # Update progress
        task_result.progress = 90
        task_result.save()
        
        # Save questions to database
        saved_count = 0
        for question_data in questions:
            try:
                # Create question with enhanced fields
                question_obj = GeneratedQuestion.objects.create(
                    file=file_obj,
                    question_text=question_data["question_text"],
                    question_type=question_data["question_type"],
                    bloom_level=question_data["bloom_level"],
                    difficulty=question_data["difficulty"],
                    answer=question_data.get("answer", ""),
                    options=question_data.get("options", []),
                    explanation=question_data.get("explanation", ""),
                    topic=question_data.get("topic", "")
                )
                
                # Set additional fields if they exist in the model
                if hasattr(question_obj, 'language'):
                    question_obj.language = question_data.get("language", language)
                if hasattr(question_obj, 'question_text_formatted'):
                    question_obj.question_text_formatted = question_data.get("question_text_formatted", question_data["question_text"])
                if hasattr(question_obj, 'answer_formatted'):
                    question_obj.answer_formatted = question_data.get("answer_formatted", question_data.get("answer", ""))
                if hasattr(question_obj, 'options_formatted'):
                    question_obj.options_formatted = question_data.get("options_formatted", question_data.get("options", []))
                if hasattr(question_obj, 'explanation_formatted'):
                    question_obj.explanation_formatted = question_data.get("explanation_formatted", question_data.get("explanation", ""))
                
                question_obj.save()
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving question: {e}")
                continue
        
        logger.info(f"Saved {saved_count} questions to database")
        
        # Complete the task
        task_result.status = 'completed'
        task_result.progress = 100
        task_result.result = {
            "questions": saved_count, 
            "file_id": file_id, 
            "language": detected_language,
            "generator_used": "real_ai",
            "bloom_levels": bloom_levels,
            "question_types": question_types
        }
        task_result.updated_at = timezone.now()
        task_result.save()
        
        logger.info(f"Task completed successfully: {saved_count} questions generated")
        
        return {
            "status": "completed", 
            "questions": saved_count, 
            "language": detected_language,
            "generator_used": "real_ai"
        }
        
    except Exception as e:
        # Handle any errors
        error_msg = str(e)
        logger.error(f"Task failed with error: {error_msg}")
        
        try:
            # Update task result with error
            task_result = TaskResult.objects.get(task_id=task_id)
            task_result.status = 'failed'
            task_result.error = error_msg
            task_result.updated_at = timezone.now()
            task_result.save()
        except Exception as save_error:
            logger.error(f"Error saving task failure: {save_error}")
        
        return {"status": "failed", "error": error_msg}