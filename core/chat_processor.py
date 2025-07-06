# core/chat_processor.py
import openai
from django.conf import settings
from .language_question_generator import LanguageSpecificQuestionGenerator
from .language_detector import LanguageDetector
import json

class ChatQuestionProcessor:
    
    def __init__(self):
        # Initialize OpenAI client if API key is available
        self.openai_available = bool(settings.OPENAI_API_KEY)
        if self.openai_available:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def process_chat_request(self, user_message: str, file_content: str, 
                           detected_language: str = 'en') -> dict:
        """Process chat request for custom questions"""
        
        # Detect language of user message
        if len(user_message) > 10:
            msg_lang_info = LanguageDetector.detect_language_advanced(user_message)
            request_language = msg_lang_info['language']
        else:
            request_language = detected_language
        
        # Parse user request to understand what type of questions they want
        request_type = self.parse_request_type(user_message, request_language)
        
        if self.openai_available and request_type['use_llm']:
            return self.generate_with_llm(user_message, file_content, request_language, request_type)
        else:
            return self.generate_with_templates(user_message, file_content, request_language, request_type)
    
    def parse_request_type(self, message: str, language: str) -> dict:
        """Parse user message to understand what they want"""
        
        message_lower = message.lower()
        
        # Request patterns by language
        patterns = {
            'en': {
                'multiple_choice': ['multiple choice', 'mcq', 'options', 'choices'],
                'short_answer': ['short answer', 'brief', 'one word', 'fill blanks'],
                'essay': ['essay', 'long answer', 'detailed', 'explain'],
                'easy': ['easy', 'simple', 'basic'],
                'medium': ['medium', 'moderate'],
                'hard': ['hard', 'difficult', 'advanced', 'complex'],
                'remembering': ['remember', 'recall', 'define', 'what is'],
                'understanding': ['understand', 'explain', 'meaning'],
                'applying': ['apply', 'use', 'example', 'how'],
                'analyzing': ['analyze', 'compare', 'examine'],
                'evaluating': ['evaluate', 'judge', 'assess'],
                'creating': ['create', 'design', 'develop']
            },
            'hi': {
                'multiple_choice': ['बहुविकल्पीय', 'विकल्प', 'mcq'],
                'short_answer': ['छोटा उत्तर', 'संक्षिप्त', 'भरें'],
                'essay': ['निबंध', 'लंबा उत्तर', 'विस्तार'],
                'easy': ['आसान', 'सरल'],
                'medium': ['मध्यम'],
                'hard': ['कठिन', 'मुश्किल'],
                'remembering': ['याद', 'परिभाषा', 'क्या है'],
                'understanding': ['समझ', 'व्याख्या', 'अर्थ'],
                'applying': ['लागू', 'उपयोग', 'उदाहरण'],
                'analyzing': ['विश्लेषण', 'तुलना'],
                'evaluating': ['मूल्यांकन', 'न्याय'],
                'creating': ['बनाना', 'रचना', 'डिज़ाइन']
            },
            'te': {
                'multiple_choice': ['బహుళ ఎంపిక', 'ఎంపికలు', 'mcq'],
                'short_answer': ['చిన్న సమాధానం', 'సంక్షిప్త'],
                'essay': ['వ్యాసం', 'పొడవైన సమాధానం'],
                'easy': ['సులభం', 'సరళం'],
                'medium': ['మధ్యమ'],
                'hard': ['కష్టం', 'క్లిష్టం'],
                'remembering': ['గుర్తుంచుకోవడం', 'నిర్వచనం'],
                'understanding': ['అవగాహన', 'వివరణ'],
                'applying': ['వర్తింపజేయడం', 'ఉపయోగం'],
                'analyzing': ['విశ్లేషణ', 'పోలిక'],
                'evaluating': ['మూల్యాంకనం'],
                'creating': ['సృష్టించడం', 'రూపకల్పన']
            },
            'ur': {
                'multiple_choice': ['متعدد انتخاب', 'اختیارات', 'mcq'],
                'short_answer': ['مختصر جواب', 'مختصر'],
                'essay': ['مضمون', 'تفصیلی جواب'],
                'easy': ['آسان', 'سادہ'],
                'medium': ['درمیانہ'],
                'hard': ['مشکل', 'پیچیدہ'],
                'remembering': ['یاد', 'تعریف'],
                'understanding': ['سمجھ', 'وضاحت'],
                'applying': ['اطلاق', 'استعمال'],
                'analyzing': ['تجزیہ', 'موازنہ'],
                'evaluating': ['تشخیص'],
                'creating': ['تخلیق', 'ڈیزائن']
            }
        }
        
        lang_patterns = patterns.get(language, patterns['en'])
        
        # Detect question type
        question_type = 'multiple_choice'  # default
        for qtype, keywords in lang_patterns.items():
            if qtype in ['multiple_choice', 'short_answer', 'essay']:
                if any(keyword in message_lower for keyword in keywords):
                    question_type = qtype
                    break
        
        # Detect difficulty
        difficulty = 'medium'  # default
        for diff, keywords in lang_patterns.items():
            if diff in ['easy', 'medium', 'hard']:
                if any(keyword in message_lower for keyword in keywords):
                    difficulty = diff
                    break
        
        # Detect Bloom level
        bloom_level = 'understanding'  # default
        for bloom, keywords in lang_patterns.items():
            if bloom in ['remembering', 'understanding', 'applying', 'analyzing', 'evaluating', 'creating']:
                if any(keyword in message_lower for keyword in keywords):
                    bloom_level = bloom
                    break
        
        # Detect if user wants to use LLM for better quality
        use_llm = any(word in message_lower for word in ['detailed', 'specific', 'custom', 'विस्तृत', 'विशिष्ट', 'तفصیلی', 'مخصوص'])
        
        return {
            'question_type': question_type,
            'difficulty': difficulty,
            'bloom_level': bloom_level,
            'use_llm': use_llm,
            'language': language
        }
    
    def generate_with_templates(self, user_message: str, file_content: str, 
                              language: str, request_type: dict) -> dict:
        """Generate questions using templates"""
        
        generator = LanguageSpecificQuestionGenerator(language=language)
        
        # Generate question based on request
        question_data = generator.generate_question(
            content=file_content,
            bloom_level=request_type['bloom_level'],
            question_type=request_type['question_type'],
            difficulty=request_type['difficulty'],
            question_number=1
        )
        
        # Format response based on language
        if language == 'hi':
            response_text = f"आपके अनुरोध के अनुसार प्रश्न:\n\n{question_data['question_text']}\n\nउत्तर: {question_data['answer']}"
        elif language == 'te':
            response_text = f"మీ అభ్యర్థన ప్రకారం ప్రశ్న:\n\n{question_data['question_text']}\n\nసమాధానం: {question_data['answer']}"
        elif language == 'ur':
            response_text = f"آپ کی درخواست کے مطابق سوال:\n\n{question_data['question_text']}\n\nجواب: {question_data['answer']}"
        else:
            response_text = f"Here's a question based on your request:\n\n{question_data['question_text']}\n\nAnswer: {question_data['answer']}"
        
        return {
            'response': response_text,
            'question_data': question_data,
            'language': language,
            'generated_by': 'template'
        }
    
    def generate_with_llm(self, user_message: str, file_content: str, 
                         language: str, request_type: dict) -> dict:
        """Generate questions using LLM for better quality"""
        
        # Language-specific prompts
        prompts = {
            'en': f"""Based on the following document content, generate a {request_type['question_type']} question at {request_type['bloom_level']} level with {request_type['difficulty']} difficulty.

User Request: {user_message}

Document Content: {file_content[:1500]}

Please provide:
1. Question text
2. Answer
3. Brief explanation

Format as JSON with keys: question, answer, explanation""",
            
            'hi': f"""निम्नलिखित दस्तावेज़ की सामग्री के आधार पर, {request_type['bloom_level']} स्तर पर {request_type['difficulty']} कठिनाई के साथ एक {request_type['question_type']} प्रश्न बनाएं।

उपयोगकर्ता अनुरोध: {user_message}

दस्तावेज़ सामग्री: {file_content[:1500]}

कृपया प्रदान करें:
1. प्रश्न पाठ
2. उत्तर  
3. संक्षिप्त स्पष्टीकरण

JSON के रूप में प्रारूपित करें: question, answer, explanation""",

            'te': f"""ఈ పత్రం కంటెంట్ ఆధారంగా, {request_type['bloom_level']} స్థాయిలో {request_type['difficulty']} కష్టతనంతో {request_type['question_type']} ప్రశ్న రూపొందించండి।

వినియోగదారు అభ్యర్థన: {user_message}

పత్రం కంటెంట్: {file_content[:1500]}

దయచేసి అందించండి:
1. ప్రశ్న టెక్స్ట్
2. సమాధానం
3. సంక్షిప్త వివరణ

JSON రూపంలో: question, answer, explanation""",

            'ur': f"""اس دستاویز کے مواد کی بنیاد پر، {request_type['bloom_level']} سطح پر {request_type['difficulty']} مشکل کے ساتھ ایک {request_type['question_type']} سوال بنائیں۔

صارف کی درخواست: {user_message}

دستاویز کا مواد: {file_content[:1500]}

براہ کرم فراہم کریں:
1. سوال کا متن
2. جواب
3. مختصر وضاحت

JSON کے طور پر: question, answer, explanation"""
        }
        
        prompt = prompts.get(language, prompts['en'])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are an expert educator creating questions in {language} language."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                import json
                response_data = json.loads(response_text)
                question_text = response_data.get('question', 'Generated question')
                answer = response_data.get('answer', 'Generated answer')
                explanation = response_data.get('explanation', 'Generated explanation')
            except:
                # Fallback if JSON parsing fails
                question_text = "LLM generated question based on your request"
                answer = "LLM generated answer"
                explanation = response_text
            
            return {
                'response': f"प्रश्न: {question_text}\n\nउत्तर: {answer}\n\nस्पष्टीकरण: {explanation}" if language == 'hi' else
                           f"ప్రశ్న: {question_text}\n\nసమాధానం: {answer}\n\nవివరణ: {explanation}" if language == 'te' else
                           f"سوال: {question_text}\n\nجواب: {answer}\n\nوضاحت: {explanation}" if language == 'ur' else
                           f"Question: {question_text}\n\nAnswer: {answer}\n\nExplanation: {explanation}",
                'question_data': {
                    'question_text': question_text,
                    'answer': answer,
                    'explanation': explanation
                },
                'language': language,
                'generated_by': 'llm'
            }
            
        except Exception as e:
            # Fallback to template method
            return self.generate_with_templates(user_message, file_content, language, request_type)