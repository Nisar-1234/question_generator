# # # # core/llm_providers.py
# # # import os
# # # from abc import ABC, abstractmethod
# # # from typing import List, Dict, Any
# # # import openai
# # # import anthropic
# # # from django.conf import settings
# # # from .models import BloomLevel, QuestionType, Difficulty
# # # import json
# # # import uuid

# # # class LLMProvider(ABC):
# # #     @abstractmethod
# # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # #         pass

# # # class OpenAIProvider(LLMProvider):
# # #     def __init__(self):
# # #         self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
# # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # #         questions = []
        
# # #         for bloom_level in request_params["bloom_levels"]:
# # #             for question_type in request_params["question_types"]:
# # #                 prompt = self._create_prompt(
# # #                     content, bloom_level, question_type, 
# # #                     request_params["difficulty"], request_params["language"], 
# # #                     request_params["num_questions_per_type"]
# # #                 )
                
# # #                 try:
# # #                     response = self.client.chat.completions.create(
# # #                         model="gpt-4o-mini",
# # #                         messages=[
# # #                             {"role": "system", "content": "You are an expert educator skilled in creating high-quality questions based on Bloom's Taxonomy."},
# # #                             {"role": "user", "content": prompt}
# # #                         ],
# # #                         temperature=0.7,
# # #                         max_tokens=2000
# # #                     )
                    
# # #                     generated_questions = self._parse_response(
# # #                         response.choices[0].message.content, 
# # #                         bloom_level, question_type, request_params["difficulty"]
# # #                     )
# # #                     questions.extend(generated_questions)
                    
# # #                 except Exception as e:
# # #                     print(f"Error generating questions: {str(e)}")
# # #                     continue
        
# # #         return questions
    
# # #     def _create_prompt(self, content: str, bloom_level: str, question_type: str, 
# # #                       difficulty: str, language: str, num_questions: int) -> str:
# # #         bloom_descriptions = {
# # #             "remembering": "recall facts, terms, basic concepts, or answers",
# # #             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting",
# # #             "applying": "use information in new situations, solve problems using required skills or knowledge",
# # #             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
# # #             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
# # #             "creating": "produce new or original work, reorganize elements into new patterns"
# # #         }
        
# # #         type_instructions = {
# # #             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Mark the correct answer.",
# # #             "short_answer": f"Create {num_questions} short answer questions (1-2 sentences expected).",
# # #             "medium_answer": f"Create {num_questions} medium answer questions (paragraph-length response expected).",
# # #             "long_answer": f"Create {num_questions} long answer questions (essay-style response expected).",
# # #             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
# # #             "true_false": f"Create {num_questions} true/false questions with explanations.",
# # #             "matching": f"Create {num_questions} matching questions with terms and definitions."
# # #         }
        
# # #         return f"""
# # # Based on the following content, create educational questions at the {bloom_level} level of Bloom's Taxonomy.

# # # BLOOM'S LEVEL: {bloom_level.title()} - {bloom_descriptions[bloom_level]}
# # # QUESTION TYPE: {question_type}
# # # DIFFICULTY: {difficulty}
# # # LANGUAGE: {language}

# # # {type_instructions[question_type]}

# # # CONTENT TO ANALYZE:
# # # {content[:3000]}

# # # INSTRUCTIONS:
# # # 1. Focus on the {bloom_level} cognitive level
# # # 2. Make questions {difficulty} difficulty
# # # 3. Respond in {language} language
# # # 4. Provide clear, unambiguous questions
# # # 5. Include answers/explanations where applicable
# # # 6. Format your response as JSON with this structure:
# # # {{
# # #     "questions": [
# # #         {{
# # #             "question": "question text",
# # #             "type": "{question_type}",
# # #             "answer": "correct answer or explanation",
# # #             "options": ["A", "B", "C", "D"],
# # #             "explanation": "why this answer is correct"
# # #         }}
# # #     ]
# # # }}
# # # """
    
# # #     def _parse_response(self, response: str, bloom_level: str, question_type: str, difficulty: str) -> List[Dict[str, Any]]:
# # #         try:
# # #             if "```json" in response:
# # #                 json_str = response.split("```json")[1].split("```")[0]
# # #             else:
# # #                 json_str = response
            
# # #             data = json.loads(json_str)
# # #             questions = []
            
# # #             for q in data.get("questions", []):
# # #                 question = {
# # #                     "id": str(uuid.uuid4()),
# # #                     "question_text": q.get("question", ""),
# # #                     "question_type": question_type,
# # #                     "bloom_level": bloom_level,
# # #                     "difficulty": difficulty,
# # #                     "answer": q.get("answer"),
# # #                     "options": q.get("options", []),
# # #                     "explanation": q.get("explanation")
# # #                 }
# # #                 questions.append(question)
            
# # #             return questions
            
# # #         except Exception as e:
# # #             print(f"Error parsing response: {str(e)}")
# # #             return []

# # # class LLMProviderFactory:
# # #     @staticmethod
# # #     def create_provider(provider_name: str) -> LLMProvider:
# # #         if provider_name == "openai":
# # #             return OpenAIProvider()
# # #         elif provider_name == "anthropic":
# # #             # Implementation for Anthropic
# # #             pass
# # #         else:
# # #             raise ValueError(f"Unsupported LLM provider: {provider_name}")


# # # core/llm_providers.py
# # import os
# # from abc import ABC, abstractmethod
# # from typing import List, Dict, Any
# # import openai
# # from django.conf import settings
# # from .models import BloomLevel, QuestionType, Difficulty
# # import json
# # import uuid

# # class LLMProvider(ABC):
# #     @abstractmethod
# #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         pass

# # class OpenAIProvider(LLMProvider):
# #     def __init__(self):
# #         # FIXED: Remove problematic parameters
# #         self.client = openai.OpenAI(
# #             api_key=settings.OPENAI_API_KEY,
# #             # Remove any proxy or other problematic parameters
# #         )
    
# #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         bloom_levels = request_params["bloom_levels"]
# #         question_types = request_params["question_types"] 
# #         difficulty = request_params["difficulty"]
# #         language = request_params.get("language", "en")
# #         num_questions = request_params["num_questions_per_type"]
        
# #         questions = []
        
# #         # TEMPORARY: Create mock questions instead of calling OpenAI
# #         # This allows testing without API key or network issues
        
# #         for bloom_level in bloom_levels:
# #             for question_type in question_types:
# #                 for i in range(num_questions):
# #                     question = {
# #                         "id": str(uuid.uuid4()),
# #                         "question_text": f"Sample {bloom_level} {question_type} question #{i+1}: What can you tell me about the main concepts in this document?",
# #                         "question_type": question_type,
# #                         "bloom_level": bloom_level,
# #                         "difficulty": difficulty,
# #                         "answer": f"This is a sample answer for a {bloom_level} level question.",
# #                         "options": ["Option A", "Option B", "Option C", "Option D"] if question_type == "multiple_choice" else [],
# #                         "explanation": f"This question tests {bloom_level} cognitive skills by asking students to demonstrate understanding."
# #                     }
# #                     questions.append(question)
        
# #         return questions
    
# #     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         """Real OpenAI implementation - use this when API key is configured"""
# #         bloom_levels = request_params["bloom_levels"]
# #         question_types = request_params["question_types"] 
# #         difficulty = request_params["difficulty"]
# #         language = request_params.get("language", "en")
# #         num_questions = request_params["num_questions_per_type"]
        
# #         questions = []
        
# #         for bloom_level in bloom_levels:
# #             for question_type in question_types:
# #                 prompt = self._create_prompt(content, bloom_level, question_type, difficulty, language, num_questions)
                
# #                 try:
# #                     response = self.client.chat.completions.create(
# #                         model="gpt-4o-mini",
# #                         messages=[
# #                             {"role": "system", "content": "You are an expert educator skilled in creating high-quality questions based on Bloom's Taxonomy."},
# #                             {"role": "user", "content": prompt}
# #                         ],
# #                         temperature=0.7,
# #                         max_tokens=2000
# #                     )
                    
# #                     generated_questions = self._parse_response(
# #                         response.choices[0].message.content, 
# #                         bloom_level, question_type, difficulty
# #                     )
# #                     questions.extend(generated_questions)
                    
# #                 except Exception as e:
# #                     print(f"Error generating questions with OpenAI: {str(e)}")
# #                     continue
        
# #         return questions
    
# #     def _create_prompt(self, content: str, bloom_level: str, question_type: str, 
# #                       difficulty: str, language: str, num_questions: int) -> str:
# #         bloom_descriptions = {
# #             "remembering": "recall facts, terms, basic concepts, or answers",
# #             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting",
# #             "applying": "use information in new situations, solve problems using required skills or knowledge",
# #             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
# #             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
# #             "creating": "produce new or original work, reorganize elements into new patterns"
# #         }
        
# #         type_instructions = {
# #             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Mark the correct answer.",
# #             "short_answer": f"Create {num_questions} short answer questions (1-2 sentences expected).",
# #             "medium_answer": f"Create {num_questions} medium answer questions (paragraph-length response expected).",
# #             "long_answer": f"Create {num_questions} long answer questions (essay-style response expected).",
# #             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
# #             "true_false": f"Create {num_questions} true/false questions with explanations.",
# #             "matching": f"Create {num_questions} matching questions with terms and definitions."
# #         }
        
# #         return f"""
# # Based on the following content, create educational questions at the {bloom_level} level of Bloom's Taxonomy.

# # BLOOM'S LEVEL: {bloom_level.title()} - {bloom_descriptions.get(bloom_level, "")}
# # QUESTION TYPE: {question_type}
# # DIFFICULTY: {difficulty}
# # LANGUAGE: {language}

# # {type_instructions.get(question_type, "")}

# # CONTENT TO ANALYZE:
# # {content[:2000]}

# # INSTRUCTIONS:
# # 1. Focus on the {bloom_level} cognitive level
# # 2. Make questions {difficulty} difficulty
# # 3. Respond in {language} language
# # 4. Provide clear, unambiguous questions
# # 5. Include answers/explanations where applicable
# # 6. Format your response as JSON with this structure:
# # {{
# #     "questions": [
# #         {{
# #             "question": "question text",
# #             "type": "{question_type}",
# #             "answer": "correct answer or explanation",
# #             "options": ["A", "B", "C", "D"],
# #             "explanation": "why this answer is correct"
# #         }}
# #     ]
# # }}
# # """
    
# #     def _parse_response(self, response: str, bloom_level: str, question_type: str, difficulty: str) -> List[Dict[str, Any]]:
# #         try:
# #             if "```json" in response:
# #                 json_str = response.split("```json")[1].split("```")[0]
# #             else:
# #                 json_str = response
            
# #             data = json.loads(json_str)
# #             questions = []
            
# #             for q in data.get("questions", []):
# #                 question = {
# #                     "id": str(uuid.uuid4()),
# #                     "question_text": q.get("question", ""),
# #                     "question_type": question_type,
# #                     "bloom_level": bloom_level,
# #                     "difficulty": difficulty,
# #                     "answer": q.get("answer"),
# #                     "options": q.get("options", []),
# #                     "explanation": q.get("explanation")
# #                 }
# #                 questions.append(question)
            
# #             return questions
            
# #         except Exception as e:
# #             print(f"Error parsing response: {str(e)}")
# #             return []

# # class LLMProviderFactory:
# #     @staticmethod
# #     def create_provider(provider_name: str) -> LLMProvider:
# #         if provider_name == "openai":
# #             return OpenAIProvider()
# #         elif provider_name == "anthropic":
# #             # Implementation for Anthropic would go here
# #             return OpenAIProvider()  # Fallback to OpenAI for now
# #         else:
# #             return OpenAIProvider()  # Default fallback



# # core/llm_providers.py
# import os
# from abc import ABC, abstractmethod
# from typing import List, Dict, Any
# import uuid
# from django.conf import settings

# class LLMProvider(ABC):
#     @abstractmethod
#     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         pass

# class OpenAIProvider(LLMProvider):
#     def __init__(self):
#         # For now, we'll use mock questions to avoid OpenAI API issues
#         self.use_mock = True
#         self.client = None
    
#     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Generate questions - using mock data for now"""
#         if self.use_mock:
#             return self._generate_mock_questions(content, request_params)
#         else:
#             return self._generate_with_openai(content, request_params)
    
#     def _generate_mock_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Generate sample questions for testing"""
#         bloom_levels = request_params.get("bloom_levels", ["remembering"])
#         question_types = request_params.get("question_types", ["multiple_choice"])
#         difficulty = request_params.get("difficulty", "medium")
#         num_questions = request_params.get("num_questions_per_type", 2)
        
#         questions = []
        
#         # Sample question templates
#         question_templates = {
#             "remembering": {
#                 "multiple_choice": "What is the main topic discussed in the document?",
#                 "short_answer": "List three key facts mentioned in the document.",
#                 "true_false": "The document discusses advanced concepts.",
#                 "fill_blanks": "The main subject of this document is ___."
#             },
#             "understanding": {
#                 "multiple_choice": "What does the author mean when they discuss the main concept?",
#                 "short_answer": "Explain the relationship between the key ideas presented.",
#                 "true_false": "The concepts presented are interconnected.",
#                 "fill_blanks": "The author explains that ___ leads to ___."
#             },
#             "applying": {
#                 "multiple_choice": "How could you apply these concepts in a real-world scenario?",
#                 "short_answer": "Describe how you would use this information to solve a problem.",
#                 "true_false": "These concepts can be applied in practical situations.",
#                 "fill_blanks": "To apply this concept, you would first ___."
#             },
#             "analyzing": {
#                 "multiple_choice": "What are the key components that make up this concept?",
#                 "short_answer": "Compare and contrast the different elements discussed.",
#                 "true_false": "The document presents multiple perspectives on the topic.",
#                 "fill_blanks": "The relationship between ___ and ___ demonstrates ___."
#             },
#             "evaluating": {
#                 "multiple_choice": "Which argument presented in the document is most convincing?",
#                 "short_answer": "Evaluate the strengths and weaknesses of the main argument.",
#                 "true_false": "The evidence presented strongly supports the conclusion.",
#                 "fill_blanks": "The most compelling evidence is ___ because ___."
#             },
#             "creating": {
#                 "multiple_choice": "What new solution could you develop based on these concepts?",
#                 "short_answer": "Design a new approach using the principles discussed.",
#                 "true_false": "These concepts could be combined to create something new.",
#                 "fill_blanks": "A new innovation might combine ___ with ___."
#             }
#         }
        
#         # Generate questions for each combination
#         for bloom_level in bloom_levels:
#             for question_type in question_types:
#                 for i in range(num_questions):
#                     # Get template or fallback
#                     template = question_templates.get(bloom_level, {}).get(question_type, 
#                         f"Sample {bloom_level} {question_type} question about the document content.")
                    
#                     # Create options for multiple choice
#                     options = []
#                     if question_type == "multiple_choice":
#                         options = [
#                             "Option A: First possible answer",
#                             "Option B: Second possible answer", 
#                             "Option C: Third possible answer",
#                             "Option D: Fourth possible answer"
#                         ]
                    
#                     # Create the question
#                     question = {
#                         "id": str(uuid.uuid4()),
#                         "question_text": f"{template} (Question {i+1})",
#                         "question_type": question_type,
#                         "bloom_level": bloom_level,
#                         "difficulty": difficulty,
#                         "answer": f"Sample answer for {bloom_level} level {question_type} question.",
#                         "options": options,
#                         "explanation": f"This question tests {bloom_level} cognitive skills by requiring students to {self._get_bloom_description(bloom_level)}."
#                     }
#                     questions.append(question)
        
#         return questions
    
#     def _get_bloom_description(self, bloom_level):
#         """Get description of what each Bloom level tests"""
#         descriptions = {
#             "remembering": "recall and recognize information",
#             "understanding": "comprehend and explain concepts",
#             "applying": "use knowledge in new situations",
#             "analyzing": "break down and examine relationships",
#             "evaluating": "make judgments and assess value",
#             "creating": "synthesize and generate new ideas"
#         }
#         return descriptions.get(bloom_level, "engage with the content")
    
#     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Real OpenAI implementation - to be used later when API is configured"""
#         # This will be implemented when you have OpenAI API key configured
#         # For now, fall back to mock questions
#         return self._generate_mock_questions(content, request_params)

# class LLMProviderFactory:
#     @staticmethod
#     def create_provider(provider_name: str) -> LLMProvider:
#         """Factory to create LLM providers"""
#         if provider_name in ["openai", "anthropic", "deepseek", "gemini"]:
#             return OpenAIProvider()  # All use OpenAI provider for now
#         else:
#             return OpenAIProvider()  # Default fallback












# core/llm_providers.py
import uuid
from typing import List, Dict, Any

class LLMProvider:
    """Base class for LLM providers"""
    def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

class MockProvider(LLMProvider):
    """Mock provider that generates sample questions without any external dependencies"""
    
    def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate realistic mock questions for testing"""
        bloom_levels = request_params.get("bloom_levels", ["remembering"])
        question_types = request_params.get("question_types", ["multiple_choice"])
        difficulty = request_params.get("difficulty", "medium")
        num_questions = request_params.get("num_questions_per_type", 2)
        
        questions = []
        
        # Question templates by Bloom level and type
        templates = {
            "remembering": {
                "multiple_choice": "What is the main topic discussed in the document?",
                "short_answer": "List three key facts mentioned in the document.",
                "true_false": "The document discusses fundamental concepts.",
                "fill_blanks": "The main subject of this document is ___.",
                "medium_answer": "Describe the primary focus of this document.",
                "long_answer": "Provide a detailed summary of the document's content.",
                "matching": "Match the following terms with their definitions."
            },
            "understanding": {
                "multiple_choice": "What does the author mean by the main concept?",
                "short_answer": "Explain the relationship between the key ideas.",
                "true_false": "The concepts presented are interconnected.",
                "fill_blanks": "The author explains that ___ leads to ___.",
                "medium_answer": "Interpret the significance of the main arguments.",
                "long_answer": "Analyze how the different concepts relate to each other.",
                "matching": "Connect the causes with their corresponding effects."
            },
            "applying": {
                "multiple_choice": "How would you apply these concepts in practice?",
                "short_answer": "Give an example of how to use this information.",
                "true_false": "These concepts can be applied in real situations.",
                "fill_blanks": "To apply this concept, you would first ___.",
                "medium_answer": "Demonstrate how to implement these ideas.",
                "long_answer": "Create a detailed plan for applying these concepts.",
                "matching": "Pair each principle with its practical application."
            },
            "analyzing": {
                "multiple_choice": "What are the key components of this concept?",
                "short_answer": "Compare the different elements discussed.",
                "true_false": "The document presents multiple perspectives.",
                "fill_blanks": "The relationship between ___ and ___ shows ___.",
                "medium_answer": "Break down the main argument into its parts.",
                "long_answer": "Examine the structure and organization of ideas.",
                "matching": "Link each component with its function."
            },
            "evaluating": {
                "multiple_choice": "Which argument is most convincing?",
                "short_answer": "Judge the effectiveness of the main points.",
                "true_false": "The evidence strongly supports the conclusion.",
                "fill_blanks": "The strongest evidence is ___ because ___.",
                "medium_answer": "Assess the quality of the arguments presented.",
                "long_answer": "Critique the document's reasoning and evidence.",
                "matching": "Evaluate each claim against its supporting evidence."
            },
            "creating": {
                "multiple_choice": "What new solution could you develop?",
                "short_answer": "Design a new approach using these principles.",
                "true_false": "These concepts could be combined innovatively.",
                "fill_blanks": "A new innovation might combine ___ with ___.",
                "medium_answer": "Propose improvements to the existing ideas.",
                "long_answer": "Synthesize the concepts into a comprehensive framework.",
                "matching": "Create new connections between different elements."
            }
        }
        
        # Generate questions
        for bloom_level in bloom_levels:
            for question_type in question_types:
                for i in range(num_questions):
                    # Get template
                    template = templates.get(bloom_level, {}).get(question_type, 
                        f"Sample {bloom_level} {question_type} question about the content.")
                    
                    # Create options for multiple choice
                    options = []
                    answer = f"Sample answer for this {bloom_level} level question."
                    
                    if question_type == "multiple_choice":
                        if bloom_level == "remembering":
                            options = [
                                "The document's primary subject matter",
                                "A secondary topic mentioned briefly", 
                                "An unrelated concept",
                                "A minor detail from the conclusion"
                            ]
                            answer = "The document's primary subject matter"
                        elif bloom_level == "understanding":
                            options = [
                                "It represents a fundamental principle",
                                "It's a contradictory statement",
                                "It's an unimportant detail",
                                "It's a typing error"
                            ]
                            answer = "It represents a fundamental principle"
                        else:
                            options = [
                                f"Option A for {bloom_level}",
                                f"Option B for {bloom_level}",
                                f"Option C for {bloom_level}",
                                f"Option D for {bloom_level}"
                            ]
                            answer = f"Option A for {bloom_level}"
                    
                    elif question_type == "true_false":
                        answer = "True"
                    
                    # Create question object
                    question = {
                        "id": str(uuid.uuid4()),
                        "question_text": f"{template} (Question {i+1})",
                        "question_type": question_type,
                        "bloom_level": bloom_level,
                        "difficulty": difficulty,
                        "answer": answer,
                        "options": options,
                        "explanation": f"This {difficulty} question tests {bloom_level} level thinking by requiring students to {self._get_skill_description(bloom_level)}."
                    }
                    questions.append(question)
        
        return questions
    
    def _get_skill_description(self, bloom_level):
        """Get description of cognitive skills for each Bloom level"""
        skills = {
            "remembering": "recall and recognize specific information",
            "understanding": "comprehend and explain concepts in their own words",
            "applying": "use knowledge and skills in new situations",
            "analyzing": "break down information and examine relationships",
            "evaluating": "make judgments and assess the value of ideas",
            "creating": "synthesize information to generate new ideas or solutions"
        }
        return skills.get(bloom_level, "engage with the content meaningfully")

class LLMProviderFactory:
    """Factory class to create LLM providers"""
    
    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        """Create an LLM provider - currently returns MockProvider for all types"""
        # For now, always return MockProvider regardless of requested provider
        # This ensures no external API dependencies
        return MockProvider()