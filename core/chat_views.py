from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
from .llm_providers import LLMProviderFactory
import json

@csrf_exempt
def chat_with_document(request, file_id):
    if request.method == 'POST':
        try:
            file_obj = get_object_or_404(UploadedFile, id=file_id)
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)
            
            # Create chat prompt
            chat_prompt = f'''
            Based on the following document content, please answer the user's question:
            
            DOCUMENT CONTENT:
            {file_obj.content[:2000]}...
            
            USER QUESTION: {user_message}
            
            Please provide a helpful and accurate answer based on the document content.
            '''
            
            # Use OpenAI provider for chat
            provider = LLMProviderFactory.create_provider('openai')
            
            # Simple chat implementation using OpenAI
            import openai
            from django.conf import settings
            
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided document content."},
                    {"role": "user", "content": chat_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            bot_response = response.choices[0].message.content
            
            return JsonResponse({
                'response': bot_response,
                'status': 'success'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
