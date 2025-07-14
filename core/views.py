# # from django.shortcuts import render
# # # core/views.py
# # from django.shortcuts import render, get_object_or_404, redirect
# # from django.contrib import messages
# # from django.http import JsonResponse, HttpResponse
# # from django.views.decorators.csrf import csrf_exempt
# # from django.utils.decorators import method_decorator
# # from django.views.generic import TemplateView
# # from rest_framework import viewsets, status
# # from rest_framework.decorators import action
# # from rest_framework.response import Response
# # from rest_framework.parsers import MultiPartParser, FormParser
# # from .models import *
# # from .serializers import *
# # from .file_processor import FileProcessor
# # from .tasks import generate_questions_task
# # import json
# # import uuid
# # import os


# # class HomeView(TemplateView):
# #     template_name = 'home.html'

# # class FileUploadView(TemplateView):
# #     template_name = 'upload.html'

# # # def upload_file(request):
# # #     if request.method == 'POST' and request.FILES.get('file'):
# # #         uploaded_file = request.FILES['file']
        
# # #         # Validate file type
# # #         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
# # #         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
# # #         if file_ext not in allowed_extensions:
# # #             messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
# # #             return redirect('upload')
        
# # #         try:
# # #             # Save file
# # #             file_obj = UploadedFile.objects.create(
# # #                 filename=uploaded_file.name,
# # #                 file=uploaded_file,
# # #                 content=""  # Will be populated by processing
# # #             )
            
# # #             # Process file
# # #             file_path = file_obj.file.path
# # #             processed_data = FileProcessor.process_file(file_path, uploaded_file.name)
            
# # #             # Update file object
# # #             file_obj.content = processed_data["content"]
# # #             file_obj.detected_language = processed_data["detected_language"]
# # #             file_obj.word_count = processed_data["word_count"]
# # #             file_obj.math_content_detected = processed_data["math_content_detected"]
# # #             file_obj.save()
            
# # #             messages.success(request, f"File uploaded successfully! Detected {file_obj.word_count} words.")
# # #             return redirect('generate', file_id=file_obj.id)
            
# # #         except Exception as e:
# # #             messages.error(request, f"Error processing file: {str(e)}")
# # #             return redirect('upload')
    
# # #     return render(request, 'upload.html')

# # # Update upload_file function in core/views.py
# # def upload_file(request):
# #     """Enhanced upload with language detection"""
# #     if request.method == 'POST' and request.FILES.get('file'):
# #         uploaded_file = request.FILES['file']
        
# #         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
# #         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
# #         if file_ext not in allowed_extensions:
# #             messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
# #             return redirect('upload')
        
# #         try:
# #             # Create file object
# #             file_obj = UploadedFile.objects.create(
# #                 filename=uploaded_file.name,
# #                 file=uploaded_file,
# #                 content="Processing..."
# #             )
            
# #             # Enhanced processing with language detection
# #             from .file_processor import EnhancedFileProcessor
# #             file_path = file_obj.file.path
# #             processed_data = EnhancedFileProcessor.process_file_with_language(file_path, uploaded_file.name)
            
# #             # Update file object with language-specific data
# #             file_obj.content = processed_data["content"]
# #             file_obj.detected_language = processed_data["detected_language"]
# #             file_obj.word_count = processed_data["word_count"]
# #             file_obj.math_content_detected = processed_data["math_content_detected"]
            
# #             # Set new fields if they exist
# #             if hasattr(file_obj, 'content_type'):
# #                 file_obj.content_type = processed_data["content_type"]
# #             if hasattr(file_obj, 'script_type'):
# #                 file_obj.script_type = processed_data["script_type"]
# #             if hasattr(file_obj, 'reading_direction'):
# #                 file_obj.reading_direction = processed_data["reading_direction"]
            
# #             file_obj.save()
            
# #             # Language-specific success message
# #             if processed_data["detected_language"] == 'hi':
# #                 success_msg = f"फ़ाइल सफलतापूर्वक अपलोड की गई! भाषा: हिंदी, शब्द: {file_obj.word_count}"
# #             elif processed_data["detected_language"] == 'te':
# #                 success_msg = f"ఫైల్ విజయవంతంగా అప్లోడ్ చేయబడింది! భాష: తెలుగు, పదాలు: {file_obj.word_count}"
# #             elif processed_data["detected_language"] == 'ur':
# #                 success_msg = f"فائل کامیابی سے اپ لوڈ ہو گئی! زبان: اردو، الفاظ: {file_obj.word_count}"
# #             else:
# #                 success_msg = f"File uploaded successfully! Language: {processed_data['detected_language']}, Words: {file_obj.word_count}"
            
# #             messages.success(request, success_msg)
# #             return redirect('generate', file_id=file_obj.id)
            
# #         except Exception as e:
# #             messages.error(request, f"Error processing file: {str(e)}")
# #             return redirect('upload')
    
# #     return render(request, 'upload.html')
# # # def upload_file(request):
# # #     """Handle file upload - SAFE VERSION"""
# # #     if request.method == 'POST' and request.FILES.get('file'):
# # #         uploaded_file = request.FILES['file']
        
# # #         # Validate file type
# # #         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
# # #         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
# # #         if file_ext not in allowed_extensions:
# # #             messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
# # #             return redirect('upload')
        
# # #         try:
# # #             # Save file with basic processing only
# # #             file_obj = UploadedFile.objects.create(
# # #                 filename=uploaded_file.name,
# # #                 file=uploaded_file,
# # #                 content=f"Content from file: {uploaded_file.name}",  # Simple placeholder
# # #                 detected_language='en',
# # #                 word_count=100,
# # #                 math_content_detected=False
# # #             )
            
# # #             # Basic file processing (safe)
# # #             try:
# # #                 file_path = file_obj.file.path
                
# # #                 # Simple text extraction
# # #                 if file_ext == '.txt':
# # #                     with open(file_path, 'r', encoding='utf-8') as f:
# # #                         content = f.read()
# # #                         file_obj.content = content
# # #                         file_obj.word_count = len(content.split())
# # #                         file_obj.save()
# # #             except Exception as e:
# # #                 print(f"File processing error: {e}")
# # #                 # Continue with placeholder content
            
# # #             messages.success(request, f"File uploaded successfully!")
# # #             return redirect('generate', file_id=file_obj.id)
            
# # #         except Exception as e:
# # #             messages.error(request, f"Error uploading file: {str(e)}")
# # #             return redirect('upload')
    
# # #     return render(request, 'upload.html')
# # def generate_questions_view(request, file_id):
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
    
# #     if request.method == 'POST':
# #         # Get form data
# #         bloom_levels = request.POST.getlist('bloom_levels')
# #         question_types = request.POST.getlist('question_types')
# #         difficulty = request.POST.get('difficulty', 'medium')
# #         language = request.POST.get('language', 'en')
# #         num_questions = int(request.POST.get('num_questions', 3))
# #         llm_provider = request.POST.get('llm_provider', 'openai')
        
# #         # Validate inputs
# #         if not bloom_levels or not question_types:
# #             messages.error(request, "Please select at least one Bloom level and question type.")
# #             return render(request, 'generate.html', {'file': file_obj})
        
# #         # Start background task
# #         request_data = {
# #             'bloom_levels': bloom_levels,
# #             'question_types': question_types,
# #             'difficulty': difficulty,
# #             'language': language,
# #             'num_questions_per_type': num_questions,
# #             'llm_provider': llm_provider
# #         }
        
# #         task = generate_questions_task.delay(str(file_id), request_data)
        
# #         return redirect('task_status', task_id=task.id)
    
# #     context = {
# #         'file': file_obj,
# #         'bloom_levels': BloomLevel.choices,
# #         'question_types': QuestionType.choices,
# #         'difficulties': Difficulty.choices,
# #         'llm_providers': LLMProvider.choices,
# #     }
    
# #     return render(request, 'generate.html', context)

# # def task_status_view(request, task_id):
# #     try:
# #         task_result = TaskResult.objects.get(task_id=task_id)
        
# #         if task_result.status == 'completed':
# #             # Get file_id from task result or questions
# #             questions = GeneratedQuestion.objects.filter(file__questions__in=[task_result.task_id])
# #             if questions.exists():
# #                 file_id = questions.first().file.id
# #                 return redirect('results', file_id=file_id)
        
# #         context = {
# #             'task_result': task_result,
# #             'task_id': task_id
# #         }
# #         return render(request, 'task_status.html', context)
        
# #     except TaskResult.DoesNotExist:
# #         messages.error(request, "Task not found.")
# #         return redirect('upload')

# # def results_view(request, file_id):
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
    
# #     # Group questions by Bloom level
# #     questions_by_bloom = {}
# #     for question in questions:
# #         bloom_level = question.get_bloom_level_display()
# #         if bloom_level not in questions_by_bloom:
# #             questions_by_bloom[bloom_level] = []
# #         questions_by_bloom[bloom_level].append(question)
    
# #     context = {
# #         'file': file_obj,
# #         'questions': questions,
# #         'questions_by_bloom': questions_by_bloom,
# #         'total_questions': questions.count()
# #     }
    
# #     return render(request, 'results.html', context)

# # def chat_view(request, file_id):
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
    
# #     context = {
# #         'file': file_obj
# #     }
    
# #     return render(request, 'chat.html', context)

# # # API Views
# # class UploadedFileViewSet(viewsets.ModelViewSet):
# #     queryset = UploadedFile.objects.all()
# #     serializer_class = UploadedFileSerializer
# #     parser_classes = (MultiPartParser, FormParser)
    
# #     def create(self, request, *args, **kwargs):
# #         uploaded_file = request.FILES.get('file')
        
# #         if not uploaded_file:
# #             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
# #         # Validate file type
# #         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
# #         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
# #         if file_ext not in allowed_extensions:
# #             return Response(
# #                 {'error': f'Unsupported file type. Allowed: {allowed_extensions}'}, 
# #                 status=status.HTTP_400_BAD_REQUEST
# #             )
        
# #         try:
# #             # Create file object
# #             file_obj = UploadedFile.objects.create(
# #                 filename=uploaded_file.name,
# #                 file=uploaded_file,
# #                 content=""
# #             )
            
# #             # Process file
# #             file_path = file_obj.file.path
# #             processed_data = FileProcessor.process_file(file_path, uploaded_file.name)
            
# #             # Update file object
# #             file_obj.content = processed_data["content"]
# #             file_obj.detected_language = processed_data["detected_language"]
# #             file_obj.word_count = processed_data["word_count"]
# #             file_obj.math_content_detected = processed_data["math_content_detected"]
# #             file_obj.save()
            
# #             serializer = self.get_serializer(file_obj)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
            
# #         except Exception as e:
# #             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # class GeneratedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
# #     serializer_class = GeneratedQuestionSerializer
    
# #     def get_queryset(self):
# #         file_id = self.request.query_params.get('file_id')
# #         if file_id:
# #             return GeneratedQuestion.objects.filter(file_id=file_id)
# #         return GeneratedQuestion.objects.all()

# # class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
# #     queryset = TaskResult.objects.all()
# #     serializer_class = TaskResultSerializer
# #     lookup_field = 'task_id'

# # @csrf_exempt
# # def generate_questions_api(request):
# #     if request.method == 'POST':
# #         try:
# #             data = json.loads(request.body)
# #             serializer = QuestionGenerationRequestSerializer(data=data)
            
# #             if serializer.is_valid():
# #                 validated_data = serializer.validated_data
                
# #                 # Check if file exists
# #                 try:
# #                     file_obj = UploadedFile.objects.get(id=validated_data['file_id'])
# #                 except UploadedFile.DoesNotExist:
# #                     return JsonResponse({'error': 'File not found'}, status=404)
                
# #                 # Start background task
# #                 task = generate_questions_task.delay(str(validated_data['file_id']), validated_data)
                
# #                 return JsonResponse({'task_id': task.id, 'status': 'started'})
# #             else:
# #                 return JsonResponse({'errors': serializer.errors}, status=400)
                
# #         except json.JSONDecodeError:
# #             return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
# #     return JsonResponse({'error': 'Method not allowed'}, status=405)

# # def get_task_status_api(request, task_id):
# #     try:
# #         task_result = TaskResult.objects.get(task_id=task_id)
# #         serializer = TaskResultSerializer(task_result)
# #         return JsonResponse(serializer.data)
# #     except TaskResult.DoesNotExist:
# #         return JsonResponse({'error': 'Task not found'}, status=404)

# # # In core/views.py, modify generate_questions_view function

# # def generate_questions_view(request, file_id):
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
    
# #     if request.method == 'POST':
# #         # Handle form submission
# #         bloom_levels = request.POST.getlist('bloom_levels')
# #         question_types = request.POST.getlist('question_types')
# #         difficulty = request.POST.get('difficulty', 'medium')
# #         language = request.POST.get('language', 'en')
# #         num_questions = int(request.POST.get('num_questions', 3))
# #         llm_provider = request.POST.get('llm_provider', 'openai')
        
# #         # Validate inputs
# #         if not bloom_levels or not question_types:
# #             messages.error(request, "Please select at least one Bloom level and question type.")
# #             # Return form with error - don't forget this return!
# #             context = {
# #                 'file': file_obj,
# #                 'bloom_levels': BloomLevel.choices,
# #                 'question_types': QuestionType.choices,
# #                 'difficulties': Difficulty.choices,
# #                 'llm_providers': LLMProvider.choices,
# #             }
# #             return render(request, 'generate.html', context)
        
# #         # Start background task
# #         request_data = {
# #             'bloom_levels': bloom_levels,
# #             'question_types': question_types,
# #             'difficulty': difficulty,
# #             'language': language,
# #             'num_questions_per_type': num_questions,
# #             'llm_provider': llm_provider
# #         }
        
# #         task = generate_questions_task.delay(str(file_id), request_data)
# #         return redirect('task_status', task_id=task.id)
    
# #     # THIS WAS MISSING - Handle GET request (initial page load)
# #     context = {
# #         'file': file_obj,
# #         'bloom_levels': BloomLevel.choices,
# #         'question_types': QuestionType.choices,
# #         'difficulties': Difficulty.choices,
# #         'llm_providers': LLMProvider.choices,
# #     }
# #     return render(request, 'generate.html', context)

# # # Add to imports at top of core/views.py
# # from django.http import HttpResponse
# # from io import BytesIO
# # import json
# # import csv

# # # Add these export functions
# # def export_questions_pdf(request, file_id):
# #     """Export questions as PDF"""
# #     from reportlab.lib.pagesizes import A4
# #     from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# #     from reportlab.lib.styles import getSampleStyleSheet
    
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
    
# #     buffer = BytesIO()
# #     doc = SimpleDocTemplate(buffer, pagesize=A4)
# #     styles = getSampleStyleSheet()
# #     elements = []
    
# #     # Title
# #     elements.append(Paragraph("Generated Questions", styles['Title']))
# #     elements.append(Paragraph(f"Document: {file_obj.filename}", styles['Normal']))
# #     elements.append(Spacer(1, 20))
    
# #     # Questions
# #     for i, q in enumerate(questions, 1):
# #         elements.append(Paragraph(f"Q{i}. {q.question_text}", styles['Heading3']))
# #         if q.options:
# #             for j, opt in enumerate(q.options):
# #                 elements.append(Paragraph(f"   {chr(65+j)}. {opt}", styles['Normal']))
# #         elements.append(Paragraph(f"Answer: {q.answer}", styles['Normal']))
# #         elements.append(Spacer(1, 12))
    
# #     doc.build(elements)
# #     pdf_data = buffer.getvalue()
# #     buffer.close()
    
# #     response = HttpResponse(pdf_data, content_type='application/pdf')
# #     response['Content-Disposition'] = f'attachment; filename="questions_{file_obj.filename}.pdf"'
# #     return response

# # def export_questions_json(request, file_id):
# #     """Export questions as JSON"""
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
    
# #     data = {
# #         'document': file_obj.filename,
# #         'total_questions': questions.count(),
# #         'questions': [
# #             {
# #                 'question': q.question_text,
# #                 'type': q.question_type,
# #                 'bloom_level': q.bloom_level,
# #                 'difficulty': q.difficulty,
# #                 'answer': q.answer,
# #                 'options': q.options,
# #                 'explanation': q.explanation
# #             } for q in questions
# #         ]
# #     }
    
# #     response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
# #     response['Content-Disposition'] = f'attachment; filename="questions_{file_obj.filename}.json"'
# #     return response

# # def export_questions_csv(request, file_id):
# #     """Export questions as CSV"""
# #     file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
    
# #     response = HttpResponse(content_type='text/csv')
# #     response['Content-Disposition'] = f'attachment; filename="questions_{file_obj.filename}.csv"'
    
# #     writer = csv.writer(response)
# #     writer.writerow(['Question', 'Type', 'Bloom Level', 'Difficulty', 'Answer', 'Options', 'Explanation'])
    
# #     for q in questions:
# #         writer.writerow([
# #             q.question_text,
# #             q.question_type,
# #             q.bloom_level,
# #             q.difficulty,
# #             q.answer,
# #             '; '.join(q.options) if q.options else '',
# #             q.explanation
# #         ])
    
# #     return response







# # # from django.shortcuts import render
# # # from django.views.generic import TemplateView
# # # from django.http import JsonResponse

# # # class HomeView(TemplateView):
# # #     template_name = 'home.html'

# # # def upload_file(request):
# # #     return render(request, 'upload.html')

# # # def chat_with_document(request, file_id):
# # #     return JsonResponse({'message': 'Chat functionality coming soon'})

# # # Add this function to core/views.py
# # def get_file_from_id(id_param):
# #     """Get file object from either file_id or task_id"""
# #     try:
# #         # First try as file_id
# #         return UploadedFile.objects.get(id=id_param)
# #     except UploadedFile.DoesNotExist:
# #         # Try finding any file with questions
# #         questions = GeneratedQuestion.objects.filter(file__isnull=False)
# #         if questions.exists():
# #             return questions.first().file
# #         raise UploadedFile.DoesNotExist("No file found")

# # # Update your export functions
# # def export_questions_pdf(request, file_id):
# #     """Export questions as PDF"""
# #     try:
# #         file_obj = get_file_from_id(file_id)
# #         questions = GeneratedQuestion.objects.filter(file=file_obj)
        
# #         # Create simple text response for now
# #         response_text = f"Generated Questions for {file_obj.filename}\n"
# #         response_text += f"Total Questions: {questions.count()}\n\n"
        
# #         for i, q in enumerate(questions, 1):
# #             response_text += f"Q{i}. {q.question_text}\n"
# #             if q.options:
# #                 for j, opt in enumerate(q.options):
# #                     response_text += f"   {chr(65+j)}. {opt}\n"
# #             response_text += f"Answer: {q.answer}\n"
# #             response_text += f"Explanation: {q.explanation}\n\n"
        
# #         response = HttpResponse(response_text, content_type='text/plain')
# #         response['Content-Disposition'] = f'attachment; filename="questions_{file_obj.filename}.txt"'
# #         return response
        
# #     except Exception as e:
# #         return HttpResponse(f"Error: {str(e)}", status=404)
    

# # def export_all_questions(request):
# #     """Export all questions as simple text"""
# #     questions = GeneratedQuestion.objects.all().order_by('-created_at')
    
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     response_text = f"All Generated Questions\nTotal: {questions.count()}\n\n"
    
# #     for i, q in enumerate(questions, 1):
# #         response_text += f"Q{i}. {q.question_text}\n"
# #         response_text += f"Type: {q.question_type} | Bloom: {q.bloom_level}\n"
# #         if q.options:
# #             for j, opt in enumerate(q.options):
# #                 response_text += f"   {chr(65+j)}. {opt}\n"
# #         response_text += f"Answer: {q.answer}\n"
# #         response_text += f"Explanation: {q.explanation}\n"
# #         response_text += "-" * 50 + "\n\n"
    
# #     response = HttpResponse(response_text, content_type='text/plain')
# #     response['Content-Disposition'] = 'attachment; filename="all_questions.txt"'
# #     return response

# # from .exporters import QuestionExporter
# # from django.http import HttpResponse
# # from django.shortcuts import get_object_or_404
# # import mimetypes

# # def export_questions_pdf(request, file_id):
# #     """Export questions as professional PDF"""
# #     try:
# #         file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     except:
# #         # Fallback: get any file with questions
# #         questions = GeneratedQuestion.objects.all()
# #         if questions.exists():
# #             file_obj = questions.first().file
# #         else:
# #             return HttpResponse("No questions found", status=404)
    
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
# #     if not questions.exists():
# #         return HttpResponse("No questions found for this file", status=404)
    
# #     exporter = QuestionExporter(questions, file_obj)
# #     pdf_buffer = exporter.export_pdf()
    
# #     response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
# #     filename = f"questions_answers_{file_obj.filename.split('.')[0]}.pdf"
# #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
# #     return response

# # def export_questions_docx(request, file_id):
# #     """Export questions as professional Word document"""
# #     try:
# #         file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     except:
# #         questions = GeneratedQuestion.objects.all()
# #         if questions.exists():
# #             file_obj = questions.first().file
# #         else:
# #             return HttpResponse("No questions found", status=404)
    
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
# #     if not questions.exists():
# #         return HttpResponse("No questions found for this file", status=404)
    
# #     exporter = QuestionExporter(questions, file_obj)
# #     docx_buffer = exporter.export_docx()
    
# #     response = HttpResponse(
# #         docx_buffer.getvalue(),
# #         content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
# #     )
# #     filename = f"questions_answers_{file_obj.filename.split('.')[0]}.docx"
# #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
# #     return response

# # def export_questions_txt(request, file_id):
# #     """Export questions as formatted text file"""
# #     try:
# #         file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     except:
# #         questions = GeneratedQuestion.objects.all()
# #         if questions.exists():
# #             file_obj = questions.first().file
# #         else:
# #             return HttpResponse("No questions found", status=404)
    
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
# #     if not questions.exists():
# #         return HttpResponse("No questions found for this file", status=404)
    
# #     exporter = QuestionExporter(questions, file_obj)
# #     txt_content = exporter.export_txt()
    
# #     response = HttpResponse(txt_content, content_type='text/plain; charset=utf-8')
# #     filename = f"questions_answers_{file_obj.filename.split('.')[0]}.txt"
# #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
# #     return response

# # def export_questions_json(request, file_id):
# #     """Export questions as structured JSON"""
# #     try:
# #         file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     except:
# #         questions = GeneratedQuestion.objects.all()
# #         if questions.exists():
# #             file_obj = questions.first().file
# #         else:
# #             return HttpResponse("No questions found", status=404)
    
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
# #     if not questions.exists():
# #         return HttpResponse("No questions found for this file", status=404)
    
# #     exporter = QuestionExporter(questions, file_obj)
# #     json_content = exporter.export_json()
    
# #     response = HttpResponse(json_content, content_type='application/json; charset=utf-8')
# #     filename = f"questions_answers_{file_obj.filename.split('.')[0]}.json"
# #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
# #     return response

# # def export_questions_csv(request, file_id):
# #     """Export questions as CSV"""
# #     try:
# #         file_obj = get_object_or_404(UploadedFile, id=file_id)
# #     except:
# #         questions = GeneratedQuestion.objects.all()
# #         if questions.exists():
# #             file_obj = questions.first().file
# #         else:
# #             return HttpResponse("No questions found", status=404)
    
# #     questions = GeneratedQuestion.objects.filter(file=file_obj)
# #     if not questions.exists():
# #         return HttpResponse("No questions found for this file", status=404)
    
# #     exporter = QuestionExporter(questions, file_obj)
# #     csv_content = exporter.export_csv()
    
# #     response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
# #     filename = f"questions_answers_{file_obj.filename.split('.')[0]}.csv"
# #     response['Content-Disposition'] = f'attachment; filename="{filename}"'
# #     return response

# # # Export ALL questions (regardless of file)
# # def export_all_questions_pdf(request):
# #     """Export all questions as PDF"""
# #     questions = GeneratedQuestion.objects.all()
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     exporter = QuestionExporter(questions)
# #     pdf_buffer = exporter.export_pdf()
    
# #     response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
# #     response['Content-Disposition'] = 'attachment; filename="all_questions_answers.pdf"'
# #     return response

# # def export_all_questions_docx(request):
# #     """Export all questions as Word document"""
# #     questions = GeneratedQuestion.objects.all()
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     exporter = QuestionExporter(questions)
# #     docx_buffer = exporter.export_docx()
    
# #     response = HttpResponse(
# #         docx_buffer.getvalue(),
# #         content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
# #     )
# #     response['Content-Disposition'] = 'attachment; filename="all_questions_answers.docx"'
# #     return response

# # def export_all_questions_txt(request):
# #     """Export all questions as text file"""
# #     questions = GeneratedQuestion.objects.all()
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     exporter = QuestionExporter(questions)
# #     txt_content = exporter.export_txt()
    
# #     response = HttpResponse(txt_content, content_type='text/plain; charset=utf-8')
# #     response['Content-Disposition'] = 'attachment; filename="all_questions_answers.txt"'
# #     return response

# # def export_all_questions_json(request):
# #     """Export all questions as JSON"""
# #     questions = GeneratedQuestion.objects.all()
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     exporter = QuestionExporter(questions)
# #     json_content = exporter.export_json()
    
# #     response = HttpResponse(json_content, content_type='application/json; charset=utf-8')
# #     response['Content-Disposition'] = 'attachment; filename="all_questions_answers.json"'
# #     return response

# # def export_all_questions_csv(request):
# #     """Export all questions as CSV"""
# #     questions = GeneratedQuestion.objects.all()
# #     if not questions.exists():
# #         return HttpResponse("No questions found", status=404)
    
# #     exporter = QuestionExporter(questions)
# #     csv_content = exporter.export_csv()
    
# #     response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
# #     response['Content-Disposition'] = 'attachment; filename="all_questions_answers.csv"'
# #     return response
# # # Add to core/views.py
# # from .multilingual_generator import EnhancedLLMProviderFactory
# # from .file_processor import EnhancedFileProcessor

# # def upload_file_enhanced(request):
# #     """Enhanced file upload with multi-language support"""
# #     if request.method == 'POST' and request.FILES.get('file'):
# #         uploaded_file = request.FILES['file']
        
# #         # Validate file type
# #         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
# #         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
# #         if file_ext not in allowed_extensions:
# #             messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
# #             return redirect('upload')
        
# #         try:
# #             # Save file
# #             file_obj = UploadedFile.objects.create(
# #                 filename=uploaded_file.name,
# #                 file=uploaded_file,
# #                 content=""  # Will be populated by processing
# #             )
            
# #             # Enhanced processing
# #             file_path = file_obj.file.path
# #             processed_data = EnhancedFileProcessor.process_file_enhanced(file_path, uploaded_file.name)
            
# #             # Update file object with enhanced data
# #             file_obj.content = processed_data["content"]
# #             file_obj.detected_language = processed_data["detected_language"]
# #             file_obj.script_type = processed_data["script_type"]
# #             file_obj.reading_direction = processed_data["reading_direction"]
# #             file_obj.word_count = processed_data["word_count"]
# #             file_obj.math_content_detected = processed_data["math_content_detected"]
# #             file_obj.content_type = processed_data["content_type"]
# #             file_obj.mathematical_level = processed_data["mathematical_level"]
# #             file_obj.save()
            
# #             success_msg = f"File uploaded successfully! Detected: {processed_data['word_count']} words, "
# #             success_msg += f"Language: {processed_data['detected_language']}, "
# #             success_msg += f"Math content: {'Yes' if processed_data['math_content_detected'] else 'No'}"
            
# #             messages.success(request, success_msg)
# #             return redirect('generate', file_id=file_obj.id)
            
# #         except Exception as e:
# #             messages.error(request, f"Error processing file: {str(e)}")
# #             return redirect('upload')
    
# #     return render(request, 'upload.html')
# # # Update chat_with_document function in core/views.py
# # @csrf_exempt
# # def chat_with_document(request, file_id):
# #     """Enhanced chat with language-specific question generation"""
# #     if request.method == 'POST':
# #         try:
# #             file_obj = get_object_or_404(UploadedFile, id=file_id)
# #             data = json.loads(request.body)
# #             user_message = data.get('message', '')
            
# #             if not user_message:
# #                 return JsonResponse({'error': 'No message provided'}, status=400)
            
# #             # Use the chat processor for intelligent responses
# #             from .chat_processor import ChatQuestionProcessor
# #             chat_processor = ChatQuestionProcessor()
            
# #             # Process the chat request in the same language as the document
# #             result = chat_processor.process_chat_request(
# #                 user_message=user_message,
# #                 file_content=file_obj.content,
# #                 detected_language=file_obj.detected_language
# #             )
            
# #             return JsonResponse({
# #                 'response': result['response'],
# #                 'language': result['language'],
# #                 'generated_by': result['generated_by'],
# #                 'status': 'success'
# #             })
            
# #         except Exception as e:
# #             return JsonResponse({'error': str(e)}, status=500)
    
# #     return JsonResponse({'error': 'Method not allowed'}, status=405)

# # # Add to core/views.py
# # @csrf_exempt
# # def chat_with_document(request, file_id):
# #     """Simple chat for testing"""
# #     if request.method == 'POST':
# #         try:
# #             file_obj = get_object_or_404(UploadedFile, id=file_id)
# #             data = json.loads(request.body)
# #             user_message = data.get('message', '')
            
# #             # Simple language detection
# #             detected_lang = getattr(file_obj, 'detected_language', 'en')
            
# #             # Simple responses based on detected language
# #             if detected_lang == 'hi':
# #                 if 'कठिन' in user_message or 'मुश्किल' in user_message:
# #                     response = "प्रश्न: शिक्षा के सामाजिक प्रभावों का विस्तृत विश्लेषण करें।\nउत्तर: शिक्षा समाज में व्यापक परिवर्तन लाती है..."
# #                 elif 'आसान' in user_message or 'सरल' in user_message:
# #                     response = "प्रश्न: शिक्षा क्या है?\nउत्तर: शिक्षा ज्ञान प्राप्त करने की प्रक्रिया है।"
# #                 else:
# #                     response = f"आपका संदेश: {user_message}\nयह आपके दस्तावेज़ '{file_obj.filename}' पर आधारित एक प्रश्न है।"
                    
# #             elif detected_lang == 'te':
# #                 if 'కష్టమైన' in user_message or 'కష్టం' in user_message:
# #                     response = "ప్రశ్న: విద్య యొక్క సామాజిక ప్రభావాలను వివరించండి।\nసమాధానం: విద్య సమాజంలో విస్తృత మార్పులను తెస్తుంది..."
# #                 elif 'సులభమైన' in user_message or 'సులభం' in user_message:
# #                     response = "ప్రశ్న: విద్య అంటే ఏమిటి?\nసమాధానం: విద్య అంటే జ్ఞానం పొందే ప్రక్రియ."
# #                 else:
# #                     response = f"మీ సందేశం: {user_message}\nఇది మీ పత్రం '{file_obj.filename}' ఆధారంగా ప్రశ్న."
                    
# #             elif detected_lang == 'ur':
# #                 if 'مشکل' in user_message or 'کٹھن' in user_message:
# #                     response = "سوال: تعلیم کے سماجی اثرات کا تجزیہ کریں۔\nجواب: تعلیم معاشرے میں وسیع تبدیلیاں لاتی ہے..."
# #                 elif 'آسان' in user_message or 'سادہ' in user_message:
# #                     response = "سوال: تعلیم کیا ہے؟\nجواب: تعلیم علم حاصل کرنے کا عمل ہے۔"
# #                 else:
# #                     response = f"آپ کا پیغام: {user_message}\nیہ آپ کی دستاویز '{file_obj.filename}' پر مبنی سوال ہے۔"
# #             else:
# #                 response = f"Your message: {user_message}\nHere's a question based on your document '{file_obj.filename}'."
            
# #             return JsonResponse({
# #                 'response': response,
# #                 'language': detected_lang,
# #                 'status': 'success'
# #             })
            
# #         except Exception as e:
# #             return JsonResponse({'error': str(e)}, status=500)
    
# #     return JsonResponse({'error': 'Method not allowed'}, status=405)


# # # Add these views to core/views.py

# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # import json

# # @csrf_exempt
# # def test_ai_integration(request):
# #     """Test AI integration endpoint"""
# #     if request.method == 'POST':
# #         try:
# #             from .llm_providers import LLMProviderFactory
# #             from django.conf import settings
            
# #             # Test content
# #             test_content = """
# #             Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can analyze data, identify patterns, and make predictions or decisions. There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data. Reinforcement learning involves learning through trial and error with rewards and penalties.
# #             """
            
# #             # Test parameters
# #             test_params = {
# #                 'bloom_levels': ['remembering', 'understanding'],
# #                 'question_types': ['multiple_choice', 'short_answer'],
# #                 'difficulty': 'medium',
# #                 'num_questions_per_type': 1,
# #                 'language': 'en'
# #             }
            
# #             # Check OpenAI availability
# #             openai_status = {
# #                 'api_key_configured': bool(settings.OPENAI_API_KEY),
# #                 'api_key_preview': f"{settings.OPENAI_API_KEY[:10]}..." if settings.OPENAI_API_KEY else "Not set"
# #             }
            
# #             # Test provider creation
# #             provider = LLMProviderFactory.create_provider('openai')
# #             provider_info = {
# #                 'type': type(provider).__name__,
# #                 'use_openai': getattr(provider, 'use_openai', False)
# #             }
            
# #             # Generate test questions
# #             questions = provider.generate_questions(test_content, test_params)
            
# #             return JsonResponse({
# #                 'status': 'success',
# #                 'openai_status': openai_status,
# #                 'provider_info': provider_info,
# #                 'questions_generated': len(questions),
# #                 'questions': questions[:2],  # First 2 questions for preview
# #                 'test_content_length': len(test_content)
# #             })
            
# #         except Exception as e:
# #             return JsonResponse({
# #                 'status': 'error',
# #                 'error': str(e),
# #                 'error_type': type(e).__name__
# #             })
    
# #     return JsonResponse({'error': 'Method not allowed'}, status=405)

# # @csrf_exempt
# # def check_ai_status(request):
# #     """Check AI integration status"""
# #     try:
# #         from django.conf import settings
# #         import openai
        
# #         status = {
# #             'openai_api_key_set': bool(settings.OPENAI_API_KEY),
# #             'openai_module_available': True,
# #             'settings_debug': settings.DEBUG,
# #         }
        
# #         if settings.OPENAI_API_KEY:
# #             try:
# #                 # Test a simple OpenAI call
# #                 client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                
# #                 # Make a simple test call
# #                 response = client.chat.completions.create(
# #                     model="gpt-4o-mini",
# #                     messages=[{"role": "user", "content": "Say 'AI integration test successful'"}],
# #                     max_tokens=10
# #                 )
                
# #                 status['openai_test_call'] = 'success'
# #                 status['openai_response'] = response.choices[0].message.content
                
# #             except Exception as e:
# #                 status['openai_test_call'] = 'failed'
# #                 status['openai_error'] = str(e)
        
# #         return JsonResponse(status)
        
# #     except ImportError as e:
# #         return JsonResponse({
# #             'openai_module_available': False,
# #             'import_error': str(e)
# #         })
# #     except Exception as e:
# #         return JsonResponse({
# #             'status': 'error',
# #             'error': str(e)
# #         })

# # # Add these URL patterns to core/urls.py
# # def add_debug_urls():
# #     """Add these to your core/urls.py urlpatterns list"""
# #     return [
# #         path('debug/test-ai/', views.test_ai_integration, name='test_ai'),
# #         path('debug/ai-status/', views.check_ai_status, name='ai_status'),
# #     ]







# # core/views.py - Complete Updated File
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from .models import *
# from .serializers import *
# from .file_processor import EnhancedFileProcessor
# from .tasks import generate_questions_task
# import json
# import uuid
# import os


# class HomeView(TemplateView):
#     template_name = 'home.html'

# class FileUploadView(TemplateView):
#     template_name = 'upload.html'

# def upload_file(request):
#     """Enhanced upload with language detection"""
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
        
#         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
#         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
#         if file_ext not in allowed_extensions:
#             messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
#             return redirect('upload')
        
#         try:
#             # Create file object
#             file_obj = UploadedFile.objects.create(
#                 filename=uploaded_file.name,
#                 file=uploaded_file,
#                 content="Processing..."
#             )
            
#             # Enhanced processing with language detection
#             file_path = file_obj.file.path
#             print(f"Processing file: {file_path}")
            
#             try:
#                 processed_data = EnhancedFileProcessor.process_file_with_language(file_path, uploaded_file.name)
                
#                 # Update file object with language-specific data
#                 file_obj.content = processed_data["content"]
#                 file_obj.detected_language = processed_data["detected_language"]
#                 file_obj.word_count = processed_data["word_count"]
#                 file_obj.math_content_detected = processed_data["math_content_detected"]
                
#                 # Set enhanced fields if they exist
#                 if hasattr(file_obj, 'content_type'):
#                     file_obj.content_type = processed_data.get("content_type", "text")
#                 if hasattr(file_obj, 'script_type'):
#                     file_obj.script_type = processed_data.get("script_type", "latin")
#                 if hasattr(file_obj, 'reading_direction'):
#                     file_obj.reading_direction = processed_data.get("reading_direction", "ltr")
#                 if hasattr(file_obj, 'mathematical_level'):
#                     file_obj.mathematical_level = processed_data.get("mathematical_level", "")
                
#                 file_obj.save()
                
#                 # Language-specific success message
#                 lang = processed_data["detected_language"]
#                 if lang == 'hi':
#                     success_msg = f"फ़ाइल सफलतापूर्वक अपलोड की गई! भाषा: हिंदी, शब्द: {file_obj.word_count}"
#                 elif lang == 'te':
#                     success_msg = f"ఫైల్ విజయవంతంగా అప్లోడ్ చేయబడింది! భాష: తెలుగు, పదాలు: {file_obj.word_count}"
#                 elif lang == 'ur':
#                     success_msg = f"فائل کامیابی سے اپ لوڈ ہو گئی! زبان: اردو، الفاظ: {file_obj.word_count}"
#                 else:
#                     success_msg = f"File uploaded successfully! Language: {lang}, Words: {file_obj.word_count}"
                
#                 messages.success(request, success_msg)
#                 return redirect('generate', file_id=file_obj.id)
                
#             except Exception as e:
#                 print(f"File processing error: {e}")
#                 # Fallback processing
#                 file_obj.content = f"Content from file: {uploaded_file.name}"
#                 file_obj.detected_language = 'en'
#                 file_obj.word_count = 100
#                 file_obj.save()
                
#                 messages.warning(request, f"File uploaded with basic processing. Error: {str(e)}")
#                 return redirect('generate', file_id=file_obj.id)
            
#         except Exception as e:
#             messages.error(request, f"Error uploading file: {str(e)}")
#             return redirect('upload')
    
#     return render(request, 'upload.html')

# def generate_questions_view(request, file_id):
#     file_obj = get_object_or_404(UploadedFile, id=file_id)
    
#     if request.method == 'POST':
#         # Get form data
#         bloom_levels = request.POST.getlist('bloom_levels')
#         question_types = request.POST.getlist('question_types')
#         difficulty = request.POST.get('difficulty', 'medium')
#         language = request.POST.get('language', file_obj.detected_language)
#         num_questions = int(request.POST.get('num_questions', 3))
#         llm_provider = request.POST.get('llm_provider', 'openai')
        
#         # Validate inputs
#         if not bloom_levels or not question_types:
#             messages.error(request, "Please select at least one Bloom level and question type.")
#             context = {
#                 'file': file_obj,
#                 'bloom_levels': BloomLevel.choices,
#                 'question_types': QuestionType.choices,
#                 'difficulties': Difficulty.choices,
#                 'llm_providers': LLMProvider.choices,
#             }
#             return render(request, 'generate.html', context)
        
#         # Start background task
#         request_data = {
#             'bloom_levels': bloom_levels,
#             'question_types': question_types,
#             'difficulty': difficulty,
#             'language': language,
#             'num_questions_per_type': num_questions,
#             'llm_provider': llm_provider
#         }
        
#         print(f"Starting question generation task with data: {request_data}")
#         task = generate_questions_task.delay(str(file_id), request_data)
#         print(f"Task started with ID: {task.id}")
        
#         return redirect('task_status', task_id=task.id)
    
#     # Handle GET request (initial page load)
#     context = {
#         'file': file_obj,
#         'bloom_levels': BloomLevel.choices,
#         'question_types': QuestionType.choices,
#         'difficulties': Difficulty.choices,
#         'llm_providers': LLMProvider.choices,
#     }
#     return render(request, 'generate.html', context)

# def task_status_view(request, task_id):
#     try:
#         task_result = TaskResult.objects.get(task_id=task_id)
        
#         if task_result.status == 'completed':
#             # Get file_id from task result
#             file_id = task_result.result.get('file_id') if task_result.result else None
#             if file_id:
#                 return redirect('results', file_id=file_id)
#             else:
#                 # Fallback: find any questions and redirect to first file
#                 questions = GeneratedQuestion.objects.filter().order_by('-created_at')
#                 if questions.exists():
#                     return redirect('results', file_id=questions.first().file.id)
        
#         context = {
#             'task_result': task_result,
#             'task_id': task_id
#         }
#         return render(request, 'task_status.html', context)
        
#     except TaskResult.DoesNotExist:
#         messages.error(request, "Task not found.")
#         return redirect('upload')

# def results_view(request, file_id):
#     file_obj = get_object_or_404(UploadedFile, id=file_id)
#     questions = GeneratedQuestion.objects.filter(file=file_obj)
    
#     # Group questions by Bloom level
#     questions_by_bloom = {}
#     for question in questions:
#         bloom_level = question.get_bloom_level_display()
#         if bloom_level not in questions_by_bloom:
#             questions_by_bloom[bloom_level] = []
#         questions_by_bloom[bloom_level].append(question)
    
#     context = {
#         'file': file_obj,
#         'questions': questions,
#         'questions_by_bloom': questions_by_bloom,
#         'total_questions': questions.count()
#     }
    
#     return render(request, 'results.html', context)

# def chat_view(request, file_id):
#     file_obj = get_object_or_404(UploadedFile, id=file_id)
    
#     context = {
#         'file': file_obj
#     }
    
#     return render(request, 'chat.html', context)

# # API Views
# class UploadedFileViewSet(viewsets.ModelViewSet):
#     queryset = UploadedFile.objects.all()
#     serializer_class = UploadedFileSerializer
#     parser_classes = (MultiPartParser, FormParser)
    
#     def create(self, request, *args, **kwargs):
#         uploaded_file = request.FILES.get('file')
        
#         if not uploaded_file:
#             return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Validate file type
#         allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
#         file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
#         if file_ext not in allowed_extensions:
#             return Response(
#                 {'error': f'Unsupported file type. Allowed: {allowed_extensions}'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             # Create file object
#             file_obj = UploadedFile.objects.create(
#                 filename=uploaded_file.name,
#                 file=uploaded_file,
#                 content=""
#             )
            
#             # Process file
#             file_path = file_obj.file.path
#             processed_data = EnhancedFileProcessor.process_file_with_language(file_path, uploaded_file.name)
            
#             # Update file object
#             file_obj.content = processed_data["content"]
#             file_obj.detected_language = processed_data["detected_language"]
#             file_obj.word_count = processed_data["word_count"]
#             file_obj.math_content_detected = processed_data["math_content_detected"]
#             file_obj.save()
            
#             serializer = self.get_serializer(file_obj)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
            
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class GeneratedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = Generate




# core/views.py - Complete Updated File
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import *
from .serializers import *
from .file_processor import EnhancedFileProcessor
from .tasks import generate_questions_task
import json
import uuid
import os


class HomeView(TemplateView):
    template_name = 'home.html'

class FileUploadView(TemplateView):
    template_name = 'upload.html'

def upload_file(request):
    """Enhanced upload with language detection"""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
        file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
        if file_ext not in allowed_extensions:
            messages.error(request, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
            return redirect('upload')
        
        try:
            # Create file object
            file_obj = UploadedFile.objects.create(
                filename=uploaded_file.name,
                file=uploaded_file,
                content="Processing..."
            )
            
            # Enhanced processing with language detection
            file_path = file_obj.file.path
            print(f"Processing file: {file_path}")
            
            try:
                processed_data = EnhancedFileProcessor.process_file_with_language(file_path, uploaded_file.name)
                
                # Update file object with language-specific data
                file_obj.content = processed_data["content"]
                file_obj.detected_language = processed_data["detected_language"]
                file_obj.word_count = processed_data["word_count"]
                file_obj.math_content_detected = processed_data["math_content_detected"]
                
                # Set enhanced fields if they exist
                if hasattr(file_obj, 'content_type'):
                    file_obj.content_type = processed_data.get("content_type", "text")
                if hasattr(file_obj, 'script_type'):
                    file_obj.script_type = processed_data.get("script_type", "latin")
                if hasattr(file_obj, 'reading_direction'):
                    file_obj.reading_direction = processed_data.get("reading_direction", "ltr")
                if hasattr(file_obj, 'mathematical_level'):
                    file_obj.mathematical_level = processed_data.get("mathematical_level", "")
                
                file_obj.save()
                
                # Language-specific success message
                lang = processed_data["detected_language"]
                if lang == 'hi':
                    success_msg = f"फ़ाइल सफलतापूर्वक अपलोड की गई! भाषा: हिंदी, शब्द: {file_obj.word_count}"
                elif lang == 'te':
                    success_msg = f"ఫైల్ విజయవంతంగా అప్లోడ్ చేయబడింది! భాష: తెలుగు, పదాలు: {file_obj.word_count}"
                elif lang == 'ur':
                    success_msg = f"فائل کامیابی سے اپ لوڈ ہو گئی! زبان: اردو، الفاظ: {file_obj.word_count}"
                else:
                    success_msg = f"File uploaded successfully! Language: {lang}, Words: {file_obj.word_count}"
                
                messages.success(request, success_msg)
                return redirect('generate', file_id=file_obj.id)
                
            except Exception as e:
                print(f"File processing error: {e}")
                # Fallback processing
                file_obj.content = f"Content from file: {uploaded_file.name}"
                file_obj.detected_language = 'en'
                file_obj.word_count = 100
                file_obj.save()
                
                messages.warning(request, f"File uploaded with basic processing. Error: {str(e)}")
                return redirect('generate', file_id=file_obj.id)
            
        except Exception as e:
            messages.error(request, f"Error uploading file: {str(e)}")
            return redirect('upload')
    
    return render(request, 'upload.html')

def generate_questions_view(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    
    if request.method == 'POST':
        # Get form data
        bloom_levels = request.POST.getlist('bloom_levels')
        question_types = request.POST.getlist('question_types')
        difficulty = request.POST.get('difficulty', 'medium')
        language = request.POST.get('language', file_obj.detected_language)
        num_questions = int(request.POST.get('num_questions', 3))
        llm_provider = request.POST.get('llm_provider', 'openai')
        
        # Validate inputs
        if not bloom_levels or not question_types:
            messages.error(request, "Please select at least one Bloom level and question type.")
            context = {
                'file': file_obj,
                'bloom_levels': BloomLevel.choices,
                'question_types': QuestionType.choices,
                'difficulties': Difficulty.choices,
                'llm_providers': LLMProvider.choices,
            }
            return render(request, 'generate.html', context)
        
        # Start background task
        request_data = {
            'bloom_levels': bloom_levels,
            'question_types': question_types,
            'difficulty': difficulty,
            'language': language,
            'num_questions_per_type': num_questions,
            'llm_provider': llm_provider
        }
        
        print(f"Starting question generation task with data: {request_data}")
        task = generate_questions_task.delay(str(file_id), request_data)
        print(f"Task started with ID: {task.id}")
        
        return redirect('task_status', task_id=task.id)
    
    # Handle GET request (initial page load)
    context = {
        'file': file_obj,
        'bloom_levels': BloomLevel.choices,
        'question_types': QuestionType.choices,
        'difficulties': Difficulty.choices,
        'llm_providers': LLMProvider.choices,
    }
    return render(request, 'generate.html', context)

def task_status_view(request, task_id):
    try:
        task_result = TaskResult.objects.get(task_id=task_id)
        
        if task_result.status == 'completed':
            # Get file_id from task result
            file_id = task_result.result.get('file_id') if task_result.result else None
            if file_id:
                return redirect('results', file_id=file_id)
            else:
                # Fallback: find any questions and redirect to first file
                questions = GeneratedQuestion.objects.filter().order_by('-created_at')
                if questions.exists():
                    return redirect('results', file_id=questions.first().file.id)
        
        context = {
            'task_result': task_result,
            'task_id': task_id
        }
        return render(request, 'task_status.html', context)
        
    except TaskResult.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect('upload')

def results_view(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    questions = GeneratedQuestion.objects.filter(file=file_obj)
    
    # Group questions by Bloom level
    questions_by_bloom = {}
    for question in questions:
        bloom_level = question.get_bloom_level_display()
        if bloom_level not in questions_by_bloom:
            questions_by_bloom[bloom_level] = []
        questions_by_bloom[bloom_level].append(question)
    
    context = {
        'file': file_obj,
        'questions': questions,
        'questions_by_bloom': questions_by_bloom,
        'total_questions': questions.count()
    }
    
    return render(request, 'results.html', context)

def chat_view(request, file_id):
    file_obj = get_object_or_404(UploadedFile, id=file_id)
    
    context = {
        'file': file_obj
    }
    
    return render(request, 'chat.html', context)

# API Views
class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        
        if not uploaded_file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
        file_ext = '.' + uploaded_file.name.lower().split('.')[-1]
        
        if file_ext not in allowed_extensions:
            return Response(
                {'error': f'Unsupported file type. Allowed: {allowed_extensions}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Create file object
            file_obj = UploadedFile.objects.create(
                filename=uploaded_file.name,
                file=uploaded_file,
                content=""
            )
            
            # Process file
            file_path = file_obj.file.path
            processed_data = EnhancedFileProcessor.process_file_with_language(file_path, uploaded_file.name)
            
            # Update file object
            file_obj.content = processed_data["content"]
            file_obj.detected_language = processed_data["detected_language"]
            file_obj.word_count = processed_data["word_count"]
            file_obj.math_content_detected = processed_data["math_content_detected"]
            file_obj.save()
            
            serializer = self.get_serializer(file_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GeneratedQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GeneratedQuestionSerializer
    
    def get_queryset(self):
        file_id = self.request.query_params.get('file_id')
        if file_id:
            return GeneratedQuestion.objects.filter(file_id=file_id)
        return GeneratedQuestion.objects.all()

class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    lookup_field = 'task_id'

@csrf_exempt
def generate_questions_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = QuestionGenerationRequestSerializer(data=data)
            
            if serializer.is_valid():
                validated_data = serializer.validated_data
                
                # Check if file exists
                try:
                    file_obj = UploadedFile.objects.get(id=validated_data['file_id'])
                except UploadedFile.DoesNotExist:
                    return JsonResponse({'error': 'File not found'}, status=404)
                
                # Start background task
                task = generate_questions_task.delay(str(validated_data['file_id']), validated_data)
                
                return JsonResponse({'task_id': task.id, 'status': 'started'})
            else:
                return JsonResponse({'errors': serializer.errors}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def get_task_status_api(request, task_id):
    try:
        task_result = TaskResult.objects.get(task_id=task_id)
        serializer = TaskResultSerializer(task_result)
        return JsonResponse(serializer.data)
    except TaskResult.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

# Enhanced Chat Function
@csrf_exempt
def chat_with_document(request, file_id):
    """Enhanced chat with AI integration"""
    if request.method == 'POST':
        try:
            file_obj = get_object_or_404(UploadedFile, id=file_id)
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Get detected language
            detected_lang = getattr(file_obj, 'detected_language', 'en')
            
            # Try to use AI for chat if available
            try:
                from .llm_providers import LLMProviderFactory
                provider = LLMProviderFactory.create_provider('openai')
                
                # Create a simple chat prompt
                chat_prompt = f"""
                Based on this document content, please answer the user's question in {detected_lang} language:
                
                DOCUMENT CONTENT:
                {file_obj.content[:2000]}
                
                USER QUESTION: {user_message}
                
                Please provide a helpful answer in {detected_lang} language based on the document content.
                """
                
                # Generate response using the same AI system
                if hasattr(provider, 'client') and provider.client:
                    response = provider.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": f"You are a helpful assistant that answers questions based on provided document content. Always respond in {detected_lang} language."},
                            {"role": "user", "content": chat_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=500
                    )
                    
                    bot_response = response.choices[0].message.content
                    
                    return JsonResponse({
                        'response': bot_response,
                        'language': detected_lang,
                        'generated_by': 'ai',
                        'status': 'success'
                    })
                    
            except Exception as e:
                print(f"AI chat failed: {e}")
                # Fall back to simple responses
            
            # Fallback: Simple language-based responses
            if detected_lang == 'hi':
                if 'कठिन' in user_message or 'मुश्किल' in user_message:
                    response = "प्रश्न: इस दस्तावेज़ के मुख्य विषयों का विस्तृत विश्लेषण करें।\nउत्तर: दस्तावेज़ में विभिन्न महत्वपूर्ण विषयों की चर्चा की गई है..."
                elif 'आसान' in user_message or 'सरल' in user_message:
                    response = "प्रश्न: इस दस्तावेज़ का मुख्य विषय क्या है?\nउत्तर: दस्तावेज़ का मुख्य विषय संबंधित क्षेत्र की जानकारी है।"
                else:
                    response = f"आपका प्रश्न: {user_message}\n\nउत्तर: यह आपके दस्तावेज़ '{file_obj.filename}' की सामग्री पर आधारित प्रश्न है। कृपया अधिक विशिष्ट प्रश्न पूछें।"
                    
            elif detected_lang == 'te':
                if 'కష్టమైన' in user_message or 'కష్టం' in user_message:
                    response = "ప్రశ్న: ఈ పత్రంలోని ముఖ్య అంశాలను వివరంగా విశ్లేషించండి।\nసమాధానం: పత్రంలో వివిధ ముఖ్యమైన అంశాలు చర్చించబడ్డాయి..."
                elif 'సులభమైన' in user_message or 'సులభం' in user_message:
                    response = "ప్రశ్న: ఈ పత్రం యొక్క ముఖ్య అంశం ఏమిటి?\nసమాధానం: పత్రం యొక్క ముఖ్య అంశం సంబంధిత రంగం గురించిన సమాచారం."
                else:
                    response = f"మీ ప్రశ్న: {user_message}\n\nసమాధానం: ఇది మీ పత్రం '{file_obj.filename}' కంటెంట్ ఆధారంగా ప్రశ్న. దయచేసి మరింత నిర్దిష్ట ప్రశ్న అడగండి."
                    
            elif detected_lang == 'ur':
                if 'مشکل' in user_message or 'کٹھن' in user_message:
                    response = "سوال: اس دستاویز کے اہم موضوعات کا تفصیلی تجزیہ کریں۔\nجواب: دستاویز میں مختلف اہم موضوعات پر بحث کی گئی ہے..."
                elif 'آسان' in user_message or 'سادہ' in user_message:
                    response = "سوال: اس دستاویز کا بنیادی موضوع کیا ہے؟\nجواب: دستاویز کا بنیادی موضوع متعلقہ شعبے کی معلومات ہے۔"
                else:
                    response = f"آپ کا سوال: {user_message}\n\nجواب: یہ آپ کی دستاویز '{file_obj.filename}' کے مواد پر مبنی سوال ہے۔ براہ کرم زیادہ مخصوص سوال پوچھیں۔"
            else:
                response = f"Your question: {user_message}\n\nBased on your document '{file_obj.filename}', this appears to be asking about the content. Please ask more specific questions about the document."
            
            return JsonResponse({
                'response': response,
                'language': detected_lang,
                'generated_by': 'fallback',
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# Export Functions using the enhanced exporter
from .exporters import QuestionExporter

def get_file_from_id(id_param):
    """Get file object from either file_id or task_id"""
    try:
        # First try as file_id
        return UploadedFile.objects.get(id=id_param)
    except UploadedFile.DoesNotExist:
        # Try finding any file with questions
        questions = GeneratedQuestion.objects.filter(file__isnull=False)
        if questions.exists():
            return questions.first().file
        raise UploadedFile.DoesNotExist("No file found")

def export_questions_pdf(request, file_id):
    """Export questions as professional PDF"""
    try:
        file_obj = get_file_from_id(file_id)
        questions = GeneratedQuestion.objects.filter(file=file_obj)
        
        if not questions.exists():
            return HttpResponse("No questions found for this file", status=404)
        
        exporter = QuestionExporter(questions, file_obj)
        pdf_buffer = exporter.export_pdf()
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        filename = f"questions_answers_{file_obj.filename.split('.')[0]}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

def export_questions_docx(request, file_id):
    """Export questions as professional Word document"""
    try:
        file_obj = get_file_from_id(file_id)
        questions = GeneratedQuestion.objects.filter(file=file_obj)
        
        if not questions.exists():
            return HttpResponse("No questions found for this file", status=404)
        
        exporter = QuestionExporter(questions, file_obj)
        docx_buffer = exporter.export_docx()
        
        response = HttpResponse(
            docx_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        filename = f"questions_answers_{file_obj.filename.split('.')[0]}.docx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

def export_questions_txt(request, file_id):
    """Export questions as formatted text file"""
    try:
        file_obj = get_file_from_id(file_id)
        questions = GeneratedQuestion.objects.filter(file=file_obj)
        
        if not questions.exists():
            return HttpResponse("No questions found for this file", status=404)
        
        exporter = QuestionExporter(questions, file_obj)
        txt_content = exporter.export_txt()
        
        response = HttpResponse(txt_content, content_type='text/plain; charset=utf-8')
        filename = f"questions_answers_{file_obj.filename.split('.')[0]}.txt"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

def export_questions_json(request, file_id):
    """Export questions as structured JSON"""
    try:
        file_obj = get_file_from_id(file_id)
        questions = GeneratedQuestion.objects.filter(file=file_obj)
        
        if not questions.exists():
            return HttpResponse("No questions found for this file", status=404)
        
        exporter = QuestionExporter(questions, file_obj)
        json_content = exporter.export_json()
        
        response = HttpResponse(json_content, content_type='application/json; charset=utf-8')
        filename = f"questions_answers_{file_obj.filename.split('.')[0]}.json"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

def export_questions_csv(request, file_id):
    """Export questions as CSV"""
    try:
        file_obj = get_file_from_id(file_id)
        questions = GeneratedQuestion.objects.filter(file=file_obj)
        
        if not questions.exists():
            return HttpResponse("No questions found for this file", status=404)
        
        exporter = QuestionExporter(questions, file_obj)
        csv_content = exporter.export_csv()
        
        response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
        filename = f"questions_answers_{file_obj.filename.split('.')[0]}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

# Export ALL questions (regardless of file)
def export_all_questions_pdf(request):
    """Export all questions as PDF"""
    questions = GeneratedQuestion.objects.all()
    if not questions.exists():
        return HttpResponse("No questions found", status=404)
    
    exporter = QuestionExporter(questions)
    pdf_buffer = exporter.export_pdf()
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_questions_answers.pdf"'
    return response

def export_all_questions_docx(request):
    """Export all questions as Word document"""
    questions = GeneratedQuestion.objects.all()
    if not questions.exists():
        return HttpResponse("No questions found", status=404)
    
    exporter = QuestionExporter(questions)
    docx_buffer = exporter.export_docx()
    
    response = HttpResponse(
        docx_buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename="all_questions_answers.docx"'
    return response

def export_all_questions_txt(request):
    """Export all questions as text file"""
    questions = GeneratedQuestion.objects.all()
    if not questions.exists():
        return HttpResponse("No questions found", status=404)
    
    exporter = QuestionExporter(questions)
    txt_content = exporter.export_txt()
    
    response = HttpResponse(txt_content, content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="all_questions_answers.txt"'
    return response

def export_all_questions_json(request):
    """Export all questions as JSON"""
    questions = GeneratedQuestion.objects.all()
    if not questions.exists():
        return HttpResponse("No questions found", status=404)
    
    exporter = QuestionExporter(questions)
    json_content = exporter.export_json()
    
    response = HttpResponse(json_content, content_type='application/json; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="all_questions_answers.json"'
    return response

def export_all_questions_csv(request):
    """Export all questions as CSV"""
    questions = GeneratedQuestion.objects.all()
    if not questions.exists():
        return HttpResponse("No questions found", status=404)
    
    exporter = QuestionExporter(questions)
    csv_content = exporter.export_csv()
    
    response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="all_questions_answers.csv"'
    return response

# Debug and Testing Functions
@csrf_exempt
def test_ai_integration(request):
    """Test AI integration endpoint"""
    if request.method == 'POST':
        try:
            from .llm_providers import LLMProviderFactory
            from django.conf import settings
            
            # Test content from your actual uploaded file
            test_content = """
            अरुण कमल का जन्म बिहार के रोहतास जिले के नासरीगंज में 15 फरवरी 1954 को हुआ।
            ये इन दिनों पटना विश्वविद्यालय में प्राध्यापक हैं। इन्हें अपनी कविताओं के लिए साहित्य
            अकादमी पुरस्कार सहित कई अन्य पुरस्कारों से भी सम्मानित किया गया।
            """
            
            # Test parameters
            test_params = {
                'bloom_levels': ['remembering', 'understanding'],
                'question_types': ['multiple_choice', 'short_answer'],
                'difficulty': 'medium',
                'num_questions_per_type': 2,
                'language': 'hi'
            }
            
            # Check OpenAI availability
            openai_status = {
                'api_key_configured': bool(settings.OPENAI_API_KEY),
                'api_key_preview': f"{settings.OPENAI_API_KEY[:10]}..." if settings.OPENAI_API_KEY else "Not set"
            }
            
            # Test provider creation
            provider = LLMProviderFactory.create_provider('openai')
            provider_info = {
                'type': type(provider).__name__,
                'use_openai': getattr(provider, 'use_openai', False)
            }
            
            # Generate test questions
            questions = provider.generate_questions(test_content, test_params)
            
            return JsonResponse({
                'status': 'success',
                'openai_status': openai_status,
                'provider_info': provider_info,
                'questions_generated': len(questions),
                'questions': questions[:2],  # First 2 questions for preview
                'test_content_length': len(test_content)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'error_type': type(e).__name__
            })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def check_ai_status(request):
    """Check AI integration status"""
    try:
        from django.conf import settings
        
        status_info = {
            'openai_api_key_set': bool(settings.OPENAI_API_KEY),
            'settings_debug': settings.DEBUG,
        }
        
        # Try importing OpenAI
        try:
            import openai
            status_info['openai_module_available'] = True
            
            if settings.OPENAI_API_KEY:
                try:
                    # Test a simple OpenAI call
                    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": "Say 'AI integration test successful'"}],
                        max_tokens=10
                    )
                    
                    status_info['openai_test_call'] = 'success'
                    status_info['openai_response'] = response.choices[0].message.content
                    
                except Exception as e:
                    status_info['openai_test_call'] = 'failed'
                    status_info['openai_error'] = str(e)
        
        except ImportError as e:
            status_info['openai_module_available'] = False
            status_info['import_error'] = str(e)
        
        return JsonResponse(status_info)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        })
    
# Add to core/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def test_ai_integration(request):
    """Test AI integration endpoint"""
    if request.method == 'POST':
        try:
            from .llm_providers import LLMProviderFactory
            from django.conf import settings
            
            # Test content
            test_content = """
            Artificial Intelligence (AI) is transforming the world in unprecedented ways. Machine learning, 
            a subset of AI, enables computers to learn from data without explicit programming. Deep learning, 
            using neural networks, has revolutionized fields like computer vision and natural language processing. 
            AI applications include autonomous vehicles, medical diagnosis, financial fraud detection, and 
            personalized recommendations. However, AI also raises ethical concerns about privacy, bias, and 
            job displacement. The future of AI depends on responsible development and deployment.
            """
            
            # Test parameters
            test_params = {
                'bloom_levels': ['remembering', 'understanding'],
                'question_types': ['multiple_choice', 'short_answer'],
                'difficulty': 'medium',
                'num_questions_per_type': 1,
                'language': 'en'
            }
            
            # Check OpenAI availability
            openai_status = {
                'api_key_configured': bool(settings.OPENAI_API_KEY),
                'api_key_preview': f"{settings.OPENAI_API_KEY[:10]}..." if settings.OPENAI_API_KEY else "Not set"
            }
            
            # Test provider creation
            provider = LLMProviderFactory.create_provider('openai')
            provider_info = {
                'type': type(provider).__name__,
                'use_openai': getattr(provider, 'use_openai', False)
            }
            
            # Generate test questions
            questions = provider.generate_questions(test_content, test_params)
            
            return JsonResponse({
                'status': 'success',
                'openai_status': openai_status,
                'provider_info': provider_info,
                'questions_generated': len(questions),
                'questions': questions[:2],  # First 2 questions
                'test_content_preview': test_content[:200] + "..."
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'error_type': type(e).__name__
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def check_ai_status(request):
    """Check AI integration status"""
    try:
        from django.conf import settings
        import openai
        
        status = {
            'openai_api_key_set': bool(settings.OPENAI_API_KEY),
            'openai_module_available': True,
            'settings_debug': settings.DEBUG,
        }
        
        if settings.OPENAI_API_KEY:
            try:
                # Test a simple OpenAI call
                client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                
                # Make a simple test call
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": "Say 'AI test successful'"}],
                    max_tokens=10
                )
                
                status['openai_test_call'] = 'success'
                status['openai_response'] = response.choices[0].message.content
                
            except Exception as e:
                status['openai_test_call'] = 'failed'
                status['openai_error'] = str(e)
        
        return JsonResponse(status)
        
    except ImportError as e:
        return JsonResponse({
            'openai_module_available': False,
            'import_error': str(e)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        })