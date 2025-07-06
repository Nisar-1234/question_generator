# core/language_question_generator.py
import uuid
import random
from typing import List, Dict, Any

class LanguageSpecificQuestionGenerator:
    
    # Question templates by language and Bloom level
    QUESTION_TEMPLATES = {
        'en': {
            'remembering': {
                'multiple_choice': "What is {concept}?",
                'short_answer': "Define {concept}.",
                'fill_blanks': "The main idea of this document is ___.",
                'true_false': "The document discusses {topic}."
            },
            'understanding': {
                'multiple_choice': "What does the author mean by {concept}?",
                'short_answer': "Explain the main points discussed.",
                'fill_blanks': "The relationship between {concept1} and {concept2} is ___."
            },
            'applying': {
                'multiple_choice': "How would you apply {concept} in practice?",
                'short_answer': "Give an example of how to use this information.",
            },
            'analyzing': {
                'multiple_choice': "What are the key components of {concept}?",
                'short_answer': "Compare and contrast the main ideas.",
            },
            'evaluating': {
                'multiple_choice': "Which argument is most convincing?",
                'short_answer': "Evaluate the effectiveness of the main points.",
            },
            'creating': {
                'multiple_choice': "What new solution could you develop?",
                'short_answer': "Design a new approach using these concepts.",
            }
        },
        'hi': {
            'remembering': {
                'multiple_choice': "{concept} क्या है?",
                'short_answer': "{concept} को परिभाषित करें।",
                'fill_blanks': "इस दस्तावेज़ का मुख्य विचार ___ है।",
                'true_false': "दस्तावेज़ में {topic} की चर्चा की गई है।"
            },
            'understanding': {
                'multiple_choice': "लेखक का {concept} से क्या तात्पर्य है?",
                'short_answer': "मुख्य बिंदुओं को समझाएं।",
                'fill_blanks': "{concept1} और {concept2} के बीच संबंध ___ है।"
            },
            'applying': {
                'multiple_choice': "आप {concept} का व्यावहारिक उपयोग कैसे करेंगे?",
                'short_answer': "इस जानकारी का उपयोग करने का एक उदाहरण दें।",
            },
            'analyzing': {
                'multiple_choice': "{concept} के मुख्य घटक क्या हैं?",
                'short_answer': "मुख्य विचारों की तुलना और विपरीतता करें।",
            },
            'evaluating': {
                'multiple_choice': "कौन सा तर्क सबसे अधिक विश्वसनीय है?",
                'short_answer': "मुख्य बिंदुओं की प्रभावशीलता का मूल्यांकन करें।",
            },
            'creating': {
                'multiple_choice': "आप कौन सा नया समाधान विकसित कर सकते हैं?",
                'short_answer': "इन अवधारणाओं का उपयोग करके एक नया दृष्टिकोण डिज़ाइन करें।",
            }
        },
        'te': {
            'remembering': {
                'multiple_choice': "{concept} అంటే ఏమిటి?",
                'short_answer': "{concept} ను నిర్వచించండి।",
                'fill_blanks': "ఈ పత్రం యొక్క ప్రధాన ఆలోచన ___ .",
                'true_false': "పత్రంలో {topic} గురించి చర్చించబడింది."
            },
            'understanding': {
                'multiple_choice': "రచయిత {concept} అని అర్థం ఏమిటి?",
                'short_answer': "ప్రధాన అంశాలను వివరించండి।",
                'fill_blanks': "{concept1} మరియు {concept2} మధ్య సంబంధం ___ ."
            },
            'applying': {
                'multiple_choice': "మీరు {concept} ను ఆచరణలో ఎలా వర్తింపజేస్తారు?",
                'short_answer': "ఈ సమాచారాన్ని ఎలా ఉపయోగించాలో ఒక ఉదాహరణ ఇవ్వండి।",
            },
            'analyzing': {
                'multiple_choice': "{concept} యొక్క ముఖ్య భాగాలు ఏమిటి?",
                'short_answer': "ప్రధాన ఆలోచనలను పోల్చండి మరియు వ్యత్యాసాలను చూపండి।",
            },
            'evaluating': {
                'multiple_choice': "ఏ వాదన అత్యంత నమ్మదగినది?",
                'short_answer': "ప్రధాన అంశాల ప్రభావాన్ని అంచనా వేయండి।",
            },
            'creating': {
                'multiple_choice': "మీరు ఏ కొత్త పరిష్కారాన్ని అభివృద్ధి చేయగలరు?",
                'short_answer': "ఈ భావనలను ఉపయోగించి కొత్త విధానాన్ని రూపొందించండి।",
            }
        },
        'ur': {
            'remembering': {
                'multiple_choice': "{concept} کیا ہے؟",
                'short_answer': "{concept} کی تعریف کریں۔",
                'fill_blanks': "اس دستاویز کا بنیادی خیال ___ ہے۔",
                'true_false': "دستاویز میں {topic} پر بحث کی گئی ہے۔"
            },
            'understanding': {
                'multiple_choice': "مصنف کا {concept} سے کیا مطلب ہے؟",
                'short_answer': "اہم نکات کی وضاحت کریں۔",
                'fill_blanks': "{concept1} اور {concept2} کے درمیان تعلق ___ ہے۔"
            },
            'applying': {
                'multiple_choice': "آپ {concept} کو عملی طور پر کیسے استعمال کریں گے؟",
                'short_answer': "اس معلومات کا استعمال کرنے کی ایک مثال دیں۔",
            },
            'analyzing': {
                'multiple_choice': "{concept} کے اہم اجزاء کیا ہیں؟",
                'short_answer': "اہم خیالات کا موازنہ اور تضاد کریں۔",
            },
            'evaluating': {
                'multiple_choice': "کون سا دلیل سب سے زیادہ قائل کن ہے؟",
                'short_answer': "اہم نکات کی تاثیر کا جائزہ لیں۔",
            },
            'creating': {
                'multiple_choice': "آپ کون سا نیا حل تیار کر سکتے ہیں؟",
                'short_answer': "ان تصورات کا استعمال کرتے ہوئے ایک نیا طریقہ ڈیزائن کریں۔",
            }
        },
        'bn': {
            'remembering': {
                'multiple_choice': "{concept} কী?",
                'short_answer': "{concept} সংজ্ঞায়িত করুন।",
                'fill_blanks': "এই নথির মূল ভাবনা ___ ।",
                'true_false': "নথিতে {topic} নিয়ে আলোচনা করা হয়েছে।"
            }
        },
        'ta': {
            'remembering': {
                'multiple_choice': "{concept} என்றால் என்ன?",
                'short_answer': "{concept} ஐ வரையறுக்கவும்।",
                'fill_blanks': "இந்த ஆவணத்தின் முக்கிய கருத்து ___ ஆகும்।",
                'true_false': "ஆவணத்தில் {topic} பற்றி விவாதிக்கப்பட்டுள்ளது।"
            }
        }
    }
    
    # Answer templates by language
    ANSWER_TEMPLATES = {
        'en': {
            'concept_definition': "This refers to {explanation}",
            'main_point': "The main point is {point}",
            'example': "For example, {example}",
            'relationship': "The relationship shows {connection}"
        },
        'hi': {
            'concept_definition': "यह {explanation} को संदर्भित करता है",
            'main_point': "मुख्य बिंदु {point} है",
            'example': "उदाहरण के लिए, {example}",
            'relationship': "संबंध {connection} दिखाता है"
        },
        'te': {
            'concept_definition': "ఇది {explanation} ను సూచిస్తుంది",
            'main_point': "ప్రధాన అంశం {point}",
            'example': "ఉదాహరణకు, {example}",
            'relationship': "సంబంధం {connection} చూపిస్తుంది"
        },
        'ur': {
            'concept_definition': "یہ {explanation} کا حوالہ دیتا ہے",
            'main_point': "اہم نکتہ {point} ہے",
            'example': "مثال کے طور پر، {example}",
            'relationship': "رشتہ {connection} دکھاتا ہے"
        },
        'bn': {
            'concept_definition': "এটি {explanation} বোঝায়",
            'main_point': "মূল বিষয় হল {point}",
            'example': "উদাহরণস্বরূপ, {example}",
            'relationship': "সম্পর্ক {connection} দেখায়"
        }
    }
    
    def __init__(self, language='en'):
        self.language = language
    
    def generate_question(self, content: str, bloom_level: str, question_type: str, 
                         difficulty: str, question_number: int) -> Dict[str, Any]:
        """Generate a question in the specified language"""
        
        # Get templates for the language (fallback to English)
        templates = self.QUESTION_TEMPLATES.get(self.language, self.QUESTION_TEMPLATES['en'])
        bloom_templates = templates.get(bloom_level, templates['remembering'])
        template = bloom_templates.get(question_type, bloom_templates.get('multiple_choice', 
                                      "What is the main concept discussed?"))
        
        # Extract key concepts from content (simplified)
        concepts = self.extract_concepts(content)
        main_concept = concepts[0] if concepts else "the main topic"
        
        # Generate question text
        if '{concept}' in template:
            question_text = template.format(concept=main_concept)
        elif '{topic}' in template:
            question_text = template.format(topic=main_concept)
        elif '{concept1}' in template and '{concept2}' in template:
            concept1 = concepts[0] if len(concepts) > 0 else "first concept"
            concept2 = concepts[1] if len(concepts) > 1 else "second concept"
            question_text = template.format(concept1=concept1, concept2=concept2)
        else:
            question_text = template
        
        # Add question number
        question_text = f"प्रश्न {question_number}: {question_text}" if self.language == 'hi' else \
                       f"ప్రశ్న {question_number}: {question_text}" if self.language == 'te' else \
                       f"سوال {question_number}: {question_text}" if self.language == 'ur' else \
                       f"প্রশ্ন {question_number}: {question_text}" if self.language == 'bn' else \
                       f"கேள்வி {question_number}: {question_text}" if self.language == 'ta' else \
                       f"Question {question_number}: {question_text}"
        
        # Generate answer in the same language
        answer = self.generate_answer(main_concept, bloom_level)
        
        # Generate options for multiple choice
        options = []
        if question_type == 'multiple_choice':
            options = self.generate_options(answer, bloom_level)
        
        # Generate explanation
        explanation = self.generate_explanation(main_concept, answer, bloom_level)
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "language": self.language,
            "answer": answer,
            "options": options,
            "explanation": explanation,
            "has_math": False,
            "mathematical_level": "",
            "math_expressions": []
        }
    
    def extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        # Simple concept extraction (can be enhanced with NLP)
        words = content.split()
        
        # For different languages, extract meaningful words
        if self.language == 'hi':
            # Common Hindi concept words
            concepts = ['ज्ञान', 'विज्ञान', 'शिक्षा', 'समाज', 'संस्कृति', 'इतिहास']
        elif self.language == 'te':
            concepts = ['జ్ఞానం', 'విజ్ఞానం', 'విద్య', 'సమాజం', 'సంస్కృతి', 'చరిత్ర']
        elif self.language == 'ur':
            concepts = ['علم', 'سائنس', 'تعلیم', 'معاشرہ', 'ثقافت', 'تاریخ']
        else:
            concepts = ['knowledge', 'science', 'education', 'society', 'culture', 'history']
        
        # Find concepts that appear in content
        found_concepts = []
        for concept in concepts:
            if concept in content:
                found_concepts.append(concept)
        
        # If no specific concepts found, extract general terms
        if not found_concepts:
            # Extract nouns (simplified approach)
            potential_concepts = [word for word in words[:20] if len(word) > 4]
            found_concepts = potential_concepts[:3] if potential_concepts else ['मुख्य विषय' if self.language == 'hi' else 'main topic']
        
        return found_concepts
    
    def generate_answer(self, concept: str, bloom_level: str) -> str:
        """Generate answer in the specified language"""
        
        answer_templates = self.ANSWER_TEMPLATES.get(self.language, self.ANSWER_TEMPLATES['en'])
        
        if bloom_level == 'remembering':
            template = answer_templates.get('concept_definition', "This refers to {explanation}")
            return template.format(explanation=concept + " and its basic properties")
        elif bloom_level == 'understanding':
            template = answer_templates.get('main_point', "The main point is {point}")
            return template.format(point=f"understanding {concept} and its implications")
        elif bloom_level == 'applying':
            template = answer_templates.get('example', "For example, {example}")
            return template.format(example=f"we can apply {concept} in practical situations")
        else:
            return f"The answer relates to {concept} at {bloom_level} level"
    
    def generate_options(self, correct_answer: str, bloom_level: str) -> List[str]:
        """Generate multiple choice options in the specified language"""
        
        if self.language == 'hi':
            options = [
                correct_answer,
                "गलत विकल्प A",
                "गलत विकल्प B", 
                "गलत विकल्प C"
            ]
        elif self.language == 'te':
            options = [
                correct_answer,
                "తప్పు ఎంపిక A",
                "తప్పు ఎంపిక B",
                "తప్పు ఎంపిక C"
            ]
        elif self.language == 'ur':
            options = [
                correct_answer,
                "غلط انتخاب A",
                "غلط انتخاب B",
                "غلط انتخاب C"
            ]
        else:
            options = [
                correct_answer,
                "Incorrect option A",
                "Incorrect option B",
                "Incorrect option C"
            ]
        
        random.shuffle(options)
        return options
    
    def generate_explanation(self, concept: str, answer: str, bloom_level: str) -> str:
        """Generate explanation in the specified language"""
        
        if self.language == 'hi':
            return f"यह प्रश्न {bloom_level} स्तर पर {concept} की समझ का परीक्षण करता है। उत्तर: {answer}"
        elif self.language == 'te':
            return f"ఈ ప్రశ్న {bloom_level} స్థాయిలో {concept} అవగాహనను పరీక్షిస్తుంది। సమాధానం: {answer}"
        elif self.language == 'ur':
            return f"یہ سوال {bloom_level} کی سطح پر {concept} کی سمझ کو آزماتا ہے۔ جواب: {answer}"
        elif self.language == 'bn':
            return f"এই প্রশ্নটি {bloom_level} স্তরে {concept} বোঝাপড়া পরীক্ষা করে। উত্তর: {answer}"
        else:
            return f"This question tests {bloom_level} level understanding of {concept}. Answer: {answer}"