import uuid
from typing import List, Dict, Any
import random
import sympy as sp
from sympy import symbols, expand, factor, solve, diff, integrate
import numpy as np

class MultilingualMathQuestionGenerator:
    
    # Question templates in multiple languages
    QUESTION_TEMPLATES = {
        'en': {
            'remembering': {
                'multiple_choice': "What is {concept}?",
                'short_answer': "Define {concept}.",
                'fill_blanks': "The formula for {concept} is ___.",
                'mathematical': "Calculate: {expression}"
            },
            'understanding': {
                'multiple_choice': "What does {concept} represent?",
                'short_answer': "Explain the meaning of {concept}.",
                'mathematical': "Simplify: {expression}"
            },
            'applying': {
                'multiple_choice': "How would you use {concept} to solve {problem}?",
                'short_answer': "Apply {concept} to solve this problem.",
                'mathematical': "Solve for x: {equation}"
            },
            'analyzing': {
                'mathematical': "Factor the polynomial: {polynomial}",
                'multiple_choice': "What are the roots of {equation}?"
            },
            'evaluating': {
                'mathematical': "Evaluate the derivative: d/dx({function})",
                'short_answer': "Compare the effectiveness of {method1} vs {method2}."
            },
            'creating': {
                'mathematical': "Create a polynomial with roots {roots}",
                'short_answer': "Design a solution using {concept}."
            }
        },
        'hi': {
            'remembering': {
                'multiple_choice': "{concept} क्या है?",
                'short_answer': "{concept} को परिभाषित करें।",
                'fill_blanks': "{concept} का सूत्र ___ है।",
                'mathematical': "गणना करें: {expression}"
            },
            'understanding': {
                'multiple_choice': "{concept} का क्या अर्थ है?",
                'short_answer': "{concept} का अर्थ समझाएं।",
                'mathematical': "सरल करें: {expression}"
            },
            'applying': {
                'multiple_choice': "{problem} को हल करने के लिए {concept} का उपयोग कैसे करेंगे?",
                'short_answer': "इस समस्या को हल करने के लिए {concept} का प्रयोग करें।",
                'mathematical': "x के लिए हल करें: {equation}"
            }
        },
        'te': {
            'remembering': {
                'multiple_choice': "{concept} అంటే ఏమిటి?",
                'short_answer': "{concept} ను నిర్వచించండి।",
                'fill_blanks': "{concept} యొక్క సూత్రం ___ .",
                'mathematical': "లెక్కించండి: {expression}"
            },
            'understanding': {
                'multiple_choice': "{concept} దేనిని సూచిస్తుంది?",
                'short_answer': "{concept} యొక్క అర్థాన్ని వివరించండి।",
                'mathematical': "సరళీకరించండి: {expression}"
            }
        },
        'ur': {
            'remembering': {
                'multiple_choice': "{concept} کیا ہے؟",
                'short_answer': "{concept} کی تعریف کریں۔",
                'fill_blanks': "{concept} کا فارمولا ___ ہے۔",
                'mathematical': "حساب کریں: {expression}"
            },
            'understanding': {
                'mathematical': "آسان کریں: {expression}"
            }
        }
    }
    
    # Mathematical concept translations
    MATH_CONCEPTS = {
        'en': {
            'polynomial': 'polynomial',
            'quadratic': 'quadratic equation',
            'derivative': 'derivative',
            'integral': 'integral',
            'function': 'function',
            'equation': 'equation',
            'variable': 'variable',
            'coefficient': 'coefficient'
        },
        'hi': {
            'polynomial': 'बहुपद',
            'quadratic': 'द्विघात समीकरण',
            'derivative': 'अवकलज',
            'integral': 'समाकलन',
            'function': 'फलन',
            'equation': 'समीकरण',
            'variable': 'चर',
            'coefficient': 'गुणांक'
        },
        'te': {
            'polynomial': 'బహుపది',
            'quadratic': 'వర్గ సమీకరణం',
            'derivative': 'ఉత్పన్నం',
            'integral': 'సమాకలనం',
            'function': 'ఫంక్షన్',
            'equation': 'సమీకరణం',
            'variable': 'వేరియబుల్',
            'coefficient': 'గుణకం'
        },
        'ur': {
            'polynomial': 'کثیر نام',
            'quadratic': 'مربعی مساوات',
            'derivative': 'مشتق',
            'integral': 'انٹیگرل',
            'function': 'فنکشن',
            'equation': 'مساوات',
            'variable': 'متغیر',
            'coefficient': 'ضرب'
        }
    }
    
    def __init__(self, language='en'):
        self.language = language
        self.x, self.y, self.z = symbols('x y z')
    
    def generate_polynomial_question(self, difficulty='medium', question_type='multiple_choice', bloom_level='applying'):
        """Generate polynomial-related questions"""
        
        if difficulty == 'easy':
            # Simple linear or quadratic
            if random.choice([True, False]):
                # Linear: ax + b = 0
                a, b = random.randint(1, 10), random.randint(-10, 10)
                polynomial = f"{a}x + {b}"
                solution = -b/a
            else:
                # Simple quadratic: x^2 + bx + c
                b, c = random.randint(-5, 5), random.randint(-10, 10)
                polynomial = f"x^2 + {b}x + {c}"
                solutions = solve(self.x**2 + b*self.x + c, self.x)
        
        elif difficulty == 'medium':
            # Quadratic with coefficients
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-10, 10)
            polynomial = f"{a}x^2 + {b}x + {c}"
            equation = a*self.x**2 + b*self.x + c
            solutions = solve(equation, self.x)
        
        else:  # hard
            # Cubic or higher degree
            coeffs = [random.randint(-5, 5) for _ in range(4)]
            polynomial = f"{coeffs[0]}x^3 + {coeffs[1]}x^2 + {coeffs[2]}x + {coeffs[3]}"
            equation = coeffs[0]*self.x**3 + coeffs[1]*self.x**2 + coeffs[2]*self.x + coeffs[3]
            solutions = solve(equation, self.x)
        
        # Get template
        templates = self.QUESTION_TEMPLATES.get(self.language, self.QUESTION_TEMPLATES['en'])
        template = templates.get(bloom_level, {}).get(question_type, templates['remembering']['multiple_choice'])
        
        # Generate question based on Bloom level
        if bloom_level == 'remembering':
            question_text = template.format(concept=self.get_concept_translation('polynomial'))
            answer = self.get_concept_translation('polynomial') + " definition"
            
        elif bloom_level == 'understanding':
            question_text = template.format(expression=polynomial)
            # Expand and simplify
            expanded = expand(equation)
            answer = str(expanded)
            
        elif bloom_level == 'applying':
            if 'solve' in template.lower() or 'हल' in template:
                question_text = template.format(equation=f"{polynomial} = 0")
                answer = f"x = {solutions}" if solutions else "No real solutions"
            else:
                question_text = template.format(expression=polynomial)
                answer = str(expand(equation))
                
        elif bloom_level == 'analyzing':
            if 'factor' in template.lower() or 'गुणनखंड' in template:
                question_text = template.format(polynomial=polynomial)
                try:
                    factored = factor(equation)
                    answer = str(factored)
                except:
                    answer = f"Cannot factor {polynomial}"
            else:
                question_text = template.format(equation=f"{polynomial} = 0")
                answer = f"Roots: {solutions}"
                
        elif bloom_level == 'evaluating':
            if 'derivative' in template.lower() or 'अवकलज' in template:
                question_text = template.format(function=polynomial)
                derivative = diff(equation, self.x)
                answer = f"d/dx({polynomial}) = {derivative}"
            else:
                question_text = template.format(method1="factoring", method2="quadratic formula")
                answer = "Comparison of solving methods"
                
        else:  # creating
            roots_list = [random.randint(-5, 5) for _ in range(2)]
            question_text = template.format(roots=roots_list)
            # Create polynomial from roots
            poly_from_roots = (self.x - roots_list[0]) * (self.x - roots_list[1])
            answer = str(expand(poly_from_roots))
        
        # Generate options for multiple choice
        options = []
        if question_type == 'multiple_choice':
            if bloom_level == 'applying' and solutions:
                # Generate wrong options around correct answer
                correct = str(solutions[0]) if solutions else "0"
                options = [correct]
                for _ in range(3):
                    wrong = random.randint(-10, 10)
                    options.append(str(wrong))
                random.shuffle(options)
            else:
                options = [answer, "Option B", "Option C", "Option D"]
                random.shuffle(options)
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_text_formatted": f"${polynomial}$" if bloom_level != 'remembering' else question_text,
            #"question_text_formatted": f"${}$".format(polynomial) if bloom_level != 'remembering' else question_text,
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "language": self.language,
            "has_math": True,
            "mathematical_level": "algebra",
            "math_expressions": [polynomial],
            "answer": answer,
            "answer_formatted": f"${answer}$" if any(c in answer for c in ['x', '^', '+', '-', '*', '/']) else answer,
            "options": options,
            "options_formatted": [f"${opt}$" if any(c in str(opt) for c in ['x', '^', '+', '-', '*', '/']) else str(opt) for opt in options],
            "explanation": self.generate_explanation(polynomial, answer, self.language),
            "explanation_formatted": self.generate_explanation(polynomial, answer, self.language, formatted=True)
        }
    
    def generate_trigonometry_question(self, difficulty='medium', question_type='multiple_choice', bloom_level='applying'):
        """Generate trigonometry questions"""
        
        # Common angles in degrees and radians
        angles_deg = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
        angles_rad = ['0', 'π/6', 'π/4', 'π/3', 'π/2', '2π/3', '3π/4', '5π/6', 'π', '3π/2', '2π']
        
        if difficulty == 'easy':
            angle_deg = random.choice([30, 45, 60, 90])
            angle_rad = angles_rad[angles_deg.index(angle_deg)]
            func = random.choice(['sin', 'cos', 'tan'])
            
        elif difficulty == 'medium':
            angle_deg = random.choice(angles_deg[:8])  # Up to 150 degrees
            angle_rad = angles_rad[angles_deg.index(angle_deg)]
            func = random.choice(['sin', 'cos', 'tan', 'csc', 'sec', 'cot'])
            
        else:  # hard
            # Compound angles or multiple functions
            angle1 = random.choice(angles_deg[:6])
            angle2 = random.choice(angles_deg[:6])
            func = random.choice(['sin', 'cos', 'tan'])
        
        templates = self.QUESTION_TEMPLATES.get(self.language, self.QUESTION_TEMPLATES['en'])
        template = templates.get(bloom_level, {}).get('mathematical', "Calculate: {expression}")
        
        if difficulty != 'hard':
            expression = f"{func}({angle_deg}°)"
            expression_rad = f"{func}({angle_rad})"
            
            # Calculate exact values
            exact_values = {
                ('sin', 0): '0', ('sin', 30): '1/2', ('sin', 45): '√2/2', ('sin', 60): '√3/2', ('sin', 90): '1',
                ('cos', 0): '1', ('cos', 30): '√3/2', ('cos', 45): '√2/2', ('cos', 60): '1/2', ('cos', 90): '0',
                ('tan', 0): '0', ('tan', 30): '1/√3', ('tan', 45): '1', ('tan', 60): '√3', ('tan', 90): 'undefined'
            }
            
            answer = exact_values.get((func, angle_deg), "Calculate numerically")
        else:
            expression = f"{func}({angle1}° + {angle2}°)"
            answer = f"Use compound angle formula"
        
        question_text = template.format(expression=expression)
        
        # Generate options for multiple choice
        options = []
        if question_type == 'multiple_choice':
            options = [answer, "0", "1", "√2/2"]
            random.shuffle(options)
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_text_formatted": f"Calculate: ${expression_rad if 'rad' in locals() else expression}$",
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "language": self.language,
            "has_math": True,
            "mathematical_level": "trigonometry",
            "math_expressions": [expression],
            "answer": answer,
            "answer_formatted": f"${answer}$",
            "options": options,
            "options_formatted": [f"${opt}$" for opt in options],
            "explanation": f"Using trigonometric ratios and special angles",
            "explanation_formatted": f"Using trigonometric ratios and special angles: ${expression} = {answer}$"
        }
    
    def generate_calculus_question(self, difficulty='medium', question_type='short_answer', bloom_level='evaluating'):
        """Generate calculus questions"""
        
        if difficulty == 'easy':
            # Simple polynomials
            coeffs = [random.randint(1, 5), random.randint(1, 10)]
            function = f"{coeffs[0]}x^{coeffs[1]}"
            
        elif difficulty == 'medium':
            # Polynomials with multiple terms
            a, b, c = random.randint(1, 5), random.randint(1, 5), random.randint(1, 10)
            function = f"{a}x^2 + {b}x + {c}"
            
        else:  # hard
            # Trigonometric or exponential functions
            funcs = ['sin(x)', 'cos(x)', 'e^x', 'ln(x)', 'x*sin(x)']
            function = random.choice(funcs)
        
        templates = self.QUESTION_TEMPLATES.get(self.language, self.QUESTION_TEMPLATES['en'])
        template = templates.get(bloom_level, {}).get('mathematical', "Evaluate the derivative: d/dx({function})")
        
        question_text = template.format(function=function)
        
        # Calculate derivative
        try:
            if difficulty <= 2:  # easy/medium
                expr = sp.sympify(function.replace('^', '**'))
                derivative = diff(expr, self.x)
                answer = str(derivative)
            else:
                # For complex functions, provide the rule
                if 'sin' in function:
                    answer = "cos(x)" if function == "sin(x)" else "Use product rule"
                elif 'cos' in function:
                    answer = "-sin(x)" if function == "cos(x)" else "Use product rule"
                elif 'e^x' in function:
                    answer = "e^x"
                elif 'ln' in function:
                    answer = "1/x"
                else:
                    answer = "Use appropriate differentiation rules"
        except:
            answer = "Apply differentiation rules"
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_text_formatted": f"Evaluate: $\\frac{{d}}{{dx}}\\left({function}\\right)$",
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "language": self.language,
            "has_math": True,
            "mathematical_level": "calculus",
            "math_expressions": [function],
            "answer": answer,
            "answer_formatted": f"$\\frac{{d}}{{dx}}\\left({function}\\right) = {answer}$",
            "options": [],
            "options_formatted": [],
            "explanation": "Apply the rules of differentiation",
            "explanation_formatted": f"Apply the rules of differentiation to find $\\frac{{d}}{{dx}}\\left({function}\\right) = {answer}$"
        }
    
    def get_concept_translation(self, concept):
        """Get translated mathematical concept"""
        concepts = self.MATH_CONCEPTS.get(self.language, self.MATH_CONCEPTS['en'])
        return concepts.get(concept, concept)
    
    def generate_explanation(self, expression, answer, language, formatted=False):
        """Generate explanation in the specified language"""
        explanations = {
            'en': f"To solve this problem, we work with the expression {expression}. The answer is {answer}.",
            'hi': f"इस समस्या को हल करने के लिए, हम व्यंजक {expression} के साथ काम करते हैं। उत्तर {answer} है।",
            'te': f"ఈ సమస్యను పరిష్కరించడానికి, మేము వ్యక్తీకరణ {expression} తో పని చేస్తాము। సమాధానం {answer}.",
            'ur': f"اس مسئلے کو حل کرنے کے لیے، ہم اظہار {expression} کے ساتھ کام کرتے ہیں۔ جواب {answer} ہے۔"
        }
        
        explanation = explanations.get(language, explanations['en'])
        
        if formatted:
            return f"{explanation.split('.')[0]} ${expression}$. {explanation.split('.')[1]}"
        
        return explanation


# Enhanced LLM Provider for Multi-language and Math
class EnhancedLLMProvider:
    def __init__(self, language='en'):
        self.language = language
        self.math_generator = MultilingualMathQuestionGenerator(language)
    
    def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions with multi-language and math support"""
        
        bloom_levels = request_params.get("bloom_levels", ["remembering"])
        question_types = request_params.get("question_types", ["multiple_choice"])
        difficulty = request_params.get("difficulty", "medium")
        language = request_params.get("language", "en")
        num_questions = request_params.get("num_questions_per_type", 2)
        content_type = request_params.get("content_type", "text")
        mathematical_level = request_params.get("mathematical_level", "basic")
        
        # Update generator language
        self.math_generator.language = language
        
        questions = []
        
        for bloom_level in bloom_levels:
            for question_type in question_types:
                for i in range(num_questions):
                    
                    # Determine if we should generate mathematical questions
                    if content_type == 'mathematical' or 'math' in content.lower():
                        if mathematical_level in ['algebra', 'basic']:
                            question = self.math_generator.generate_polynomial_question(
                                difficulty, question_type, bloom_level
                            )
                        elif mathematical_level == 'trigonometry':
                            question = self.math_generator.generate_trigonometry_question(
                                difficulty, question_type, bloom_level
                            )
                        elif mathematical_level == 'calculus':
                            question = self.math_generator.generate_calculus_question(
                                difficulty, question_type, bloom_level
                            )
                        else:
                            question = self.generate_regular_question(
                                content, bloom_level, question_type, difficulty, language, i
                            )
                    else:
                        question = self.generate_regular_question(
                            content, bloom_level, question_type, difficulty, language, i
                        )
                    
                    questions.append(question)
        
        return questions
    
    def generate_regular_question(self, content, bloom_level, question_type, difficulty, language, index):
        """Generate regular text-based questions in multiple languages"""
        
        # Question templates by language
        question_starters = {
            'en': {
                'remembering': ["What is", "Define", "List", "Identify"],
                'understanding': ["Explain", "Describe", "Interpret", "Summarize"],
                'applying': ["How would you use", "Apply", "Demonstrate", "Solve"],
                'analyzing': ["Compare", "Contrast", "Analyze", "Examine"],
                'evaluating': ["Evaluate", "Assess", "Judge", "Critique"],
                'creating': ["Create", "Design", "Develop", "Formulate"]
            },
            'hi': {
                'remembering': ["क्या है", "परिभाषित करें", "सूची बनाएं", "पहचानें"],
                'understanding': ["समझाएं", "वर्णन करें", "व्याख्या करें", "सारांश दें"],
                'applying': ["आप कैसे उपयोग करेंगे", "लागू करें", "प्रदर्शित करें", "हल करें"],
                'analyzing': ["तुलना करें", "विपरीत करें", "विश्लेषण करें", "जांच करें"],
                'evaluating': ["मूल्यांकन करें", "आकलन करें", "न्याय करें", "समीक्षा करें"],
                'creating': ["बनाएं", "डिज़ाइन करें", "विकसित करें", "तैयार करें"]
            },
            'te': {
                'remembering': ["ఏమిటి", "నిర్వచించండి", "జాబితా చేయండి", "గుర్తించండి"],
                'understanding': ["వివరించండి", "వర్ణించండి", "వ్యాఖ్యానించండి", "సారాంశం ఇవ్వండి"],
                'applying': ["మీరు ఎలా ఉపయోగిస్తారు", "వర్తింపజేయండి", "ప్రదర్శించండి", "పరిష్కరించండి"],
                'analyzing': ["పోల్చండి", "విరుద్ధం చేయండి", "విశ్లేషించండి", "పరిశీలించండి"],
                'evaluating': ["మూల్యాంకనం చేయండి", "అంచనా వేయండి", "తీర్పు ఇవ్వండి", "విమర్శించండి"],
                'creating': ["సృష్టించండి", "రూపకల్పన చేయండి", "అభివృద్ధి చేయండి", "రూపొందించండి"]
            },
            'ur': {
                'remembering': ["کیا ہے", "تعین کریں", "فہرست بنائیں", "شناخت کریں"],
                'understanding': ["وضاحت کریں", "بیان کریں", "تشریح کریں", "خلاصہ کریں"],
                'applying': ["آپ کیسے استعمال کریں گے", "لاگو کریں", "ظاہر کریں", "حل کریں"],
                'analyzing': ["موازنہ کریں", "متضاد کریں", "تجزیہ کریں", "جانچیں"],
                'evaluating': ["جانچیں", "اندازہ لگائیں", "فیصلہ کریں", "تنقید کریں"],
                'creating': ["بنائیں", "ڈیزائن کریں", "ترقی دیں", "تیار کریں"]
            }
        }
        
        starters = question_starters.get(language, question_starters['en'])
        starter = random.choice(starters.get(bloom_level, starters['remembering']))
        
        # Generate question based on content
        content_snippet = content[:100] + "..." if len(content) > 100 else content
        
        if question_type == 'multiple_choice':
            question_text = f"{starter} the main concept discussed in this document?"
            options = ["Main concept A", "Main concept B", "Main concept C", "Main concept D"]
            answer = "Main concept A"
        else:
            question_text = f"{starter} the key points from the document."
            options = []
            answer = f"Key points related to {bloom_level} level understanding"
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_text_formatted": question_text,
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "language": language,
            "has_math": False,
            "mathematical_level": "",
            "math_expressions": [],
            "answer": answer,
            "answer_formatted": answer,
            "options": options,
            "options_formatted": options,
            "explanation": f"This {bloom_level} level question tests comprehension skills.",
            "explanation_formatted": f"This {bloom_level} level question tests comprehension skills."
        }

class EnhancedLLMProviderFactory:
    @staticmethod
    def create_provider(provider_name: str, language: str = 'en') -> EnhancedLLMProvider:
        """Create enhanced provider with language support"""
        return EnhancedLLMProvider(language)
