# # # # # # # core/llm_providers.py
# # # # # # import os
# # # # # # from abc import ABC, abstractmethod
# # # # # # from typing import List, Dict, Any
# # # # # # import openai
# # # # # # import anthropic
# # # # # # from django.conf import settings
# # # # # # from .models import BloomLevel, QuestionType, Difficulty
# # # # # # import json
# # # # # # import uuid

# # # # # # class LLMProvider(ABC):
# # # # # #     @abstractmethod
# # # # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # # # #         pass

# # # # # # class OpenAIProvider(LLMProvider):
# # # # # #     def __init__(self):
# # # # # #         self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
# # # # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # # # #         questions = []
        
# # # # # #         for bloom_level in request_params["bloom_levels"]:
# # # # # #             for question_type in request_params["question_types"]:
# # # # # #                 prompt = self._create_prompt(
# # # # # #                     content, bloom_level, question_type, 
# # # # # #                     request_params["difficulty"], request_params["language"], 
# # # # # #                     request_params["num_questions_per_type"]
# # # # # #                 )
                
# # # # # #                 try:
# # # # # #                     response = self.client.chat.completions.create(
# # # # # #                         model="gpt-4o-mini",
# # # # # #                         messages=[
# # # # # #                             {"role": "system", "content": "You are an expert educator skilled in creating high-quality questions based on Bloom's Taxonomy."},
# # # # # #                             {"role": "user", "content": prompt}
# # # # # #                         ],
# # # # # #                         temperature=0.7,
# # # # # #                         max_tokens=2000
# # # # # #                     )
                    
# # # # # #                     generated_questions = self._parse_response(
# # # # # #                         response.choices[0].message.content, 
# # # # # #                         bloom_level, question_type, request_params["difficulty"]
# # # # # #                     )
# # # # # #                     questions.extend(generated_questions)
                    
# # # # # #                 except Exception as e:
# # # # # #                     print(f"Error generating questions: {str(e)}")
# # # # # #                     continue
        
# # # # # #         return questions
    
# # # # # #     def _create_prompt(self, content: str, bloom_level: str, question_type: str, 
# # # # # #                       difficulty: str, language: str, num_questions: int) -> str:
# # # # # #         bloom_descriptions = {
# # # # # #             "remembering": "recall facts, terms, basic concepts, or answers",
# # # # # #             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting",
# # # # # #             "applying": "use information in new situations, solve problems using required skills or knowledge",
# # # # # #             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
# # # # # #             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
# # # # # #             "creating": "produce new or original work, reorganize elements into new patterns"
# # # # # #         }
        
# # # # # #         type_instructions = {
# # # # # #             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Mark the correct answer.",
# # # # # #             "short_answer": f"Create {num_questions} short answer questions (1-2 sentences expected).",
# # # # # #             "medium_answer": f"Create {num_questions} medium answer questions (paragraph-length response expected).",
# # # # # #             "long_answer": f"Create {num_questions} long answer questions (essay-style response expected).",
# # # # # #             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
# # # # # #             "true_false": f"Create {num_questions} true/false questions with explanations.",
# # # # # #             "matching": f"Create {num_questions} matching questions with terms and definitions."
# # # # # #         }
        
# # # # # #         return f"""
# # # # # # Based on the following content, create educational questions at the {bloom_level} level of Bloom's Taxonomy.

# # # # # # BLOOM'S LEVEL: {bloom_level.title()} - {bloom_descriptions[bloom_level]}
# # # # # # QUESTION TYPE: {question_type}
# # # # # # DIFFICULTY: {difficulty}
# # # # # # LANGUAGE: {language}

# # # # # # {type_instructions[question_type]}

# # # # # # CONTENT TO ANALYZE:
# # # # # # {content[:3000]}

# # # # # # INSTRUCTIONS:
# # # # # # 1. Focus on the {bloom_level} cognitive level
# # # # # # 2. Make questions {difficulty} difficulty
# # # # # # 3. Respond in {language} language
# # # # # # 4. Provide clear, unambiguous questions
# # # # # # 5. Include answers/explanations where applicable
# # # # # # 6. Format your response as JSON with this structure:
# # # # # # {{
# # # # # #     "questions": [
# # # # # #         {{
# # # # # #             "question": "question text",
# # # # # #             "type": "{question_type}",
# # # # # #             "answer": "correct answer or explanation",
# # # # # #             "options": ["A", "B", "C", "D"],
# # # # # #             "explanation": "why this answer is correct"
# # # # # #         }}
# # # # # #     ]
# # # # # # }}
# # # # # # """
    
# # # # # #     def _parse_response(self, response: str, bloom_level: str, question_type: str, difficulty: str) -> List[Dict[str, Any]]:
# # # # # #         try:
# # # # # #             if "```json" in response:
# # # # # #                 json_str = response.split("```json")[1].split("```")[0]
# # # # # #             else:
# # # # # #                 json_str = response
            
# # # # # #             data = json.loads(json_str)
# # # # # #             questions = []
            
# # # # # #             for q in data.get("questions", []):
# # # # # #                 question = {
# # # # # #                     "id": str(uuid.uuid4()),
# # # # # #                     "question_text": q.get("question", ""),
# # # # # #                     "question_type": question_type,
# # # # # #                     "bloom_level": bloom_level,
# # # # # #                     "difficulty": difficulty,
# # # # # #                     "answer": q.get("answer"),
# # # # # #                     "options": q.get("options", []),
# # # # # #                     "explanation": q.get("explanation")
# # # # # #                 }
# # # # # #                 questions.append(question)
            
# # # # # #             return questions
            
# # # # # #         except Exception as e:
# # # # # #             print(f"Error parsing response: {str(e)}")
# # # # # #             return []

# # # # # # class LLMProviderFactory:
# # # # # #     @staticmethod
# # # # # #     def create_provider(provider_name: str) -> LLMProvider:
# # # # # #         if provider_name == "openai":
# # # # # #             return OpenAIProvider()
# # # # # #         elif provider_name == "anthropic":
# # # # # #             # Implementation for Anthropic
# # # # # #             pass
# # # # # #         else:
# # # # # #             raise ValueError(f"Unsupported LLM provider: {provider_name}")


# # # # # # core/llm_providers.py
# # # # # import os
# # # # # from abc import ABC, abstractmethod
# # # # # from typing import List, Dict, Any
# # # # # import openai
# # # # # from django.conf import settings
# # # # # from .models import BloomLevel, QuestionType, Difficulty
# # # # # import json
# # # # # import uuid

# # # # # class LLMProvider(ABC):
# # # # #     @abstractmethod
# # # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # # #         pass

# # # # # class OpenAIProvider(LLMProvider):
# # # # #     def __init__(self):
# # # # #         # FIXED: Remove problematic parameters
# # # # #         self.client = openai.OpenAI(
# # # # #             api_key=settings.OPENAI_API_KEY,
# # # # #             # Remove any proxy or other problematic parameters
# # # # #         )
    
# # # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # # #         bloom_levels = request_params["bloom_levels"]
# # # # #         question_types = request_params["question_types"] 
# # # # #         difficulty = request_params["difficulty"]
# # # # #         language = request_params.get("language", "en")
# # # # #         num_questions = request_params["num_questions_per_type"]
        
# # # # #         questions = []
        
# # # # #         # TEMPORARY: Create mock questions instead of calling OpenAI
# # # # #         # This allows testing without API key or network issues
        
# # # # #         for bloom_level in bloom_levels:
# # # # #             for question_type in question_types:
# # # # #                 for i in range(num_questions):
# # # # #                     question = {
# # # # #                         "id": str(uuid.uuid4()),
# # # # #                         "question_text": f"Sample {bloom_level} {question_type} question #{i+1}: What can you tell me about the main concepts in this document?",
# # # # #                         "question_type": question_type,
# # # # #                         "bloom_level": bloom_level,
# # # # #                         "difficulty": difficulty,
# # # # #                         "answer": f"This is a sample answer for a {bloom_level} level question.",
# # # # #                         "options": ["Option A", "Option B", "Option C", "Option D"] if question_type == "multiple_choice" else [],
# # # # #                         "explanation": f"This question tests {bloom_level} cognitive skills by asking students to demonstrate understanding."
# # # # #                     }
# # # # #                     questions.append(question)
        
# # # # #         return questions
    
# # # # #     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # # #         """Real OpenAI implementation - use this when API key is configured"""
# # # # #         bloom_levels = request_params["bloom_levels"]
# # # # #         question_types = request_params["question_types"] 
# # # # #         difficulty = request_params["difficulty"]
# # # # #         language = request_params.get("language", "en")
# # # # #         num_questions = request_params["num_questions_per_type"]
        
# # # # #         questions = []
        
# # # # #         for bloom_level in bloom_levels:
# # # # #             for question_type in question_types:
# # # # #                 prompt = self._create_prompt(content, bloom_level, question_type, difficulty, language, num_questions)
                
# # # # #                 try:
# # # # #                     response = self.client.chat.completions.create(
# # # # #                         model="gpt-4o-mini",
# # # # #                         messages=[
# # # # #                             {"role": "system", "content": "You are an expert educator skilled in creating high-quality questions based on Bloom's Taxonomy."},
# # # # #                             {"role": "user", "content": prompt}
# # # # #                         ],
# # # # #                         temperature=0.7,
# # # # #                         max_tokens=2000
# # # # #                     )
                    
# # # # #                     generated_questions = self._parse_response(
# # # # #                         response.choices[0].message.content, 
# # # # #                         bloom_level, question_type, difficulty
# # # # #                     )
# # # # #                     questions.extend(generated_questions)
                    
# # # # #                 except Exception as e:
# # # # #                     print(f"Error generating questions with OpenAI: {str(e)}")
# # # # #                     continue
        
# # # # #         return questions
    
# # # # #     def _create_prompt(self, content: str, bloom_level: str, question_type: str, 
# # # # #                       difficulty: str, language: str, num_questions: int) -> str:
# # # # #         bloom_descriptions = {
# # # # #             "remembering": "recall facts, terms, basic concepts, or answers",
# # # # #             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting",
# # # # #             "applying": "use information in new situations, solve problems using required skills or knowledge",
# # # # #             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
# # # # #             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
# # # # #             "creating": "produce new or original work, reorganize elements into new patterns"
# # # # #         }
        
# # # # #         type_instructions = {
# # # # #             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Mark the correct answer.",
# # # # #             "short_answer": f"Create {num_questions} short answer questions (1-2 sentences expected).",
# # # # #             "medium_answer": f"Create {num_questions} medium answer questions (paragraph-length response expected).",
# # # # #             "long_answer": f"Create {num_questions} long answer questions (essay-style response expected).",
# # # # #             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
# # # # #             "true_false": f"Create {num_questions} true/false questions with explanations.",
# # # # #             "matching": f"Create {num_questions} matching questions with terms and definitions."
# # # # #         }
        
# # # # #         return f"""
# # # # # Based on the following content, create educational questions at the {bloom_level} level of Bloom's Taxonomy.

# # # # # BLOOM'S LEVEL: {bloom_level.title()} - {bloom_descriptions.get(bloom_level, "")}
# # # # # QUESTION TYPE: {question_type}
# # # # # DIFFICULTY: {difficulty}
# # # # # LANGUAGE: {language}

# # # # # {type_instructions.get(question_type, "")}

# # # # # CONTENT TO ANALYZE:
# # # # # {content[:2000]}

# # # # # INSTRUCTIONS:
# # # # # 1. Focus on the {bloom_level} cognitive level
# # # # # 2. Make questions {difficulty} difficulty
# # # # # 3. Respond in {language} language
# # # # # 4. Provide clear, unambiguous questions
# # # # # 5. Include answers/explanations where applicable
# # # # # 6. Format your response as JSON with this structure:
# # # # # {{
# # # # #     "questions": [
# # # # #         {{
# # # # #             "question": "question text",
# # # # #             "type": "{question_type}",
# # # # #             "answer": "correct answer or explanation",
# # # # #             "options": ["A", "B", "C", "D"],
# # # # #             "explanation": "why this answer is correct"
# # # # #         }}
# # # # #     ]
# # # # # }}
# # # # # """
    
# # # # #     def _parse_response(self, response: str, bloom_level: str, question_type: str, difficulty: str) -> List[Dict[str, Any]]:
# # # # #         try:
# # # # #             if "```json" in response:
# # # # #                 json_str = response.split("```json")[1].split("```")[0]
# # # # #             else:
# # # # #                 json_str = response
            
# # # # #             data = json.loads(json_str)
# # # # #             questions = []
            
# # # # #             for q in data.get("questions", []):
# # # # #                 question = {
# # # # #                     "id": str(uuid.uuid4()),
# # # # #                     "question_text": q.get("question", ""),
# # # # #                     "question_type": question_type,
# # # # #                     "bloom_level": bloom_level,
# # # # #                     "difficulty": difficulty,
# # # # #                     "answer": q.get("answer"),
# # # # #                     "options": q.get("options", []),
# # # # #                     "explanation": q.get("explanation")
# # # # #                 }
# # # # #                 questions.append(question)
            
# # # # #             return questions
            
# # # # #         except Exception as e:
# # # # #             print(f"Error parsing response: {str(e)}")
# # # # #             return []

# # # # # class LLMProviderFactory:
# # # # #     @staticmethod
# # # # #     def create_provider(provider_name: str) -> LLMProvider:
# # # # #         if provider_name == "openai":
# # # # #             return OpenAIProvider()
# # # # #         elif provider_name == "anthropic":
# # # # #             # Implementation for Anthropic would go here
# # # # #             return OpenAIProvider()  # Fallback to OpenAI for now
# # # # #         else:
# # # # #             return OpenAIProvider()  # Default fallback



# # # # # core/llm_providers.py
# # # # import os
# # # # from abc import ABC, abstractmethod
# # # # from typing import List, Dict, Any
# # # # import uuid
# # # # from django.conf import settings

# # # # class LLMProvider(ABC):
# # # #     @abstractmethod
# # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # #         pass

# # # # class OpenAIProvider(LLMProvider):
# # # #     def __init__(self):
# # # #         # For now, we'll use mock questions to avoid OpenAI API issues
# # # #         self.use_mock = True
# # # #         self.client = None
    
# # # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # #         """Generate questions - using mock data for now"""
# # # #         if self.use_mock:
# # # #             return self._generate_mock_questions(content, request_params)
# # # #         else:
# # # #             return self._generate_with_openai(content, request_params)
    
# # # #     def _generate_mock_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # #         """Generate sample questions for testing"""
# # # #         bloom_levels = request_params.get("bloom_levels", ["remembering"])
# # # #         question_types = request_params.get("question_types", ["multiple_choice"])
# # # #         difficulty = request_params.get("difficulty", "medium")
# # # #         num_questions = request_params.get("num_questions_per_type", 2)
        
# # # #         questions = []
        
# # # #         # Sample question templates
# # # #         question_templates = {
# # # #             "remembering": {
# # # #                 "multiple_choice": "What is the main topic discussed in the document?",
# # # #                 "short_answer": "List three key facts mentioned in the document.",
# # # #                 "true_false": "The document discusses advanced concepts.",
# # # #                 "fill_blanks": "The main subject of this document is ___."
# # # #             },
# # # #             "understanding": {
# # # #                 "multiple_choice": "What does the author mean when they discuss the main concept?",
# # # #                 "short_answer": "Explain the relationship between the key ideas presented.",
# # # #                 "true_false": "The concepts presented are interconnected.",
# # # #                 "fill_blanks": "The author explains that ___ leads to ___."
# # # #             },
# # # #             "applying": {
# # # #                 "multiple_choice": "How could you apply these concepts in a real-world scenario?",
# # # #                 "short_answer": "Describe how you would use this information to solve a problem.",
# # # #                 "true_false": "These concepts can be applied in practical situations.",
# # # #                 "fill_blanks": "To apply this concept, you would first ___."
# # # #             },
# # # #             "analyzing": {
# # # #                 "multiple_choice": "What are the key components that make up this concept?",
# # # #                 "short_answer": "Compare and contrast the different elements discussed.",
# # # #                 "true_false": "The document presents multiple perspectives on the topic.",
# # # #                 "fill_blanks": "The relationship between ___ and ___ demonstrates ___."
# # # #             },
# # # #             "evaluating": {
# # # #                 "multiple_choice": "Which argument presented in the document is most convincing?",
# # # #                 "short_answer": "Evaluate the strengths and weaknesses of the main argument.",
# # # #                 "true_false": "The evidence presented strongly supports the conclusion.",
# # # #                 "fill_blanks": "The most compelling evidence is ___ because ___."
# # # #             },
# # # #             "creating": {
# # # #                 "multiple_choice": "What new solution could you develop based on these concepts?",
# # # #                 "short_answer": "Design a new approach using the principles discussed.",
# # # #                 "true_false": "These concepts could be combined to create something new.",
# # # #                 "fill_blanks": "A new innovation might combine ___ with ___."
# # # #             }
# # # #         }
        
# # # #         # Generate questions for each combination
# # # #         for bloom_level in bloom_levels:
# # # #             for question_type in question_types:
# # # #                 for i in range(num_questions):
# # # #                     # Get template or fallback
# # # #                     template = question_templates.get(bloom_level, {}).get(question_type, 
# # # #                         f"Sample {bloom_level} {question_type} question about the document content.")
                    
# # # #                     # Create options for multiple choice
# # # #                     options = []
# # # #                     if question_type == "multiple_choice":
# # # #                         options = [
# # # #                             "Option A: First possible answer",
# # # #                             "Option B: Second possible answer", 
# # # #                             "Option C: Third possible answer",
# # # #                             "Option D: Fourth possible answer"
# # # #                         ]
                    
# # # #                     # Create the question
# # # #                     question = {
# # # #                         "id": str(uuid.uuid4()),
# # # #                         "question_text": f"{template} (Question {i+1})",
# # # #                         "question_type": question_type,
# # # #                         "bloom_level": bloom_level,
# # # #                         "difficulty": difficulty,
# # # #                         "answer": f"Sample answer for {bloom_level} level {question_type} question.",
# # # #                         "options": options,
# # # #                         "explanation": f"This question tests {bloom_level} cognitive skills by requiring students to {self._get_bloom_description(bloom_level)}."
# # # #                     }
# # # #                     questions.append(question)
        
# # # #         return questions
    
# # # #     def _get_bloom_description(self, bloom_level):
# # # #         """Get description of what each Bloom level tests"""
# # # #         descriptions = {
# # # #             "remembering": "recall and recognize information",
# # # #             "understanding": "comprehend and explain concepts",
# # # #             "applying": "use knowledge in new situations",
# # # #             "analyzing": "break down and examine relationships",
# # # #             "evaluating": "make judgments and assess value",
# # # #             "creating": "synthesize and generate new ideas"
# # # #         }
# # # #         return descriptions.get(bloom_level, "engage with the content")
    
# # # #     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # # #         """Real OpenAI implementation - to be used later when API is configured"""
# # # #         # This will be implemented when you have OpenAI API key configured
# # # #         # For now, fall back to mock questions
# # # #         return self._generate_mock_questions(content, request_params)

# # # # class LLMProviderFactory:
# # # #     @staticmethod
# # # #     def create_provider(provider_name: str) -> LLMProvider:
# # # #         """Factory to create LLM providers"""
# # # #         if provider_name in ["openai", "anthropic", "deepseek", "gemini"]:
# # # #             return OpenAIProvider()  # All use OpenAI provider for now
# # # #         else:
# # # #             return OpenAIProvider()  # Default fallback












# # # # core/llm_providers.py
# # # import uuid
# # # from typing import List, Dict, Any

# # # class LLMProvider:
# # #     """Base class for LLM providers"""
# # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # #         raise NotImplementedError

# # # class MockProvider(LLMProvider):
# # #     """Mock provider that generates sample questions without any external dependencies"""
    
# # #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# # #         """Generate realistic mock questions for testing"""
# # #         bloom_levels = request_params.get("bloom_levels", ["remembering"])
# # #         question_types = request_params.get("question_types", ["multiple_choice"])
# # #         difficulty = request_params.get("difficulty", "medium")
# # #         num_questions = request_params.get("num_questions_per_type", 2)
        
# # #         questions = []
        
# # #         # Question templates by Bloom level and type
# # #         templates = {
# # #             "remembering": {
# # #                 "multiple_choice": "What is the main topic discussed in the document?",
# # #                 "short_answer": "List three key facts mentioned in the document.",
# # #                 "true_false": "The document discusses fundamental concepts.",
# # #                 "fill_blanks": "The main subject of this document is ___.",
# # #                 "medium_answer": "Describe the primary focus of this document.",
# # #                 "long_answer": "Provide a detailed summary of the document's content.",
# # #                 "matching": "Match the following terms with their definitions."
# # #             },
# # #             "understanding": {
# # #                 "multiple_choice": "What does the author mean by the main concept?",
# # #                 "short_answer": "Explain the relationship between the key ideas.",
# # #                 "true_false": "The concepts presented are interconnected.",
# # #                 "fill_blanks": "The author explains that ___ leads to ___.",
# # #                 "medium_answer": "Interpret the significance of the main arguments.",
# # #                 "long_answer": "Analyze how the different concepts relate to each other.",
# # #                 "matching": "Connect the causes with their corresponding effects."
# # #             },
# # #             "applying": {
# # #                 "multiple_choice": "How would you apply these concepts in practice?",
# # #                 "short_answer": "Give an example of how to use this information.",
# # #                 "true_false": "These concepts can be applied in real situations.",
# # #                 "fill_blanks": "To apply this concept, you would first ___.",
# # #                 "medium_answer": "Demonstrate how to implement these ideas.",
# # #                 "long_answer": "Create a detailed plan for applying these concepts.",
# # #                 "matching": "Pair each principle with its practical application."
# # #             },
# # #             "analyzing": {
# # #                 "multiple_choice": "What are the key components of this concept?",
# # #                 "short_answer": "Compare the different elements discussed.",
# # #                 "true_false": "The document presents multiple perspectives.",
# # #                 "fill_blanks": "The relationship between ___ and ___ shows ___.",
# # #                 "medium_answer": "Break down the main argument into its parts.",
# # #                 "long_answer": "Examine the structure and organization of ideas.",
# # #                 "matching": "Link each component with its function."
# # #             },
# # #             "evaluating": {
# # #                 "multiple_choice": "Which argument is most convincing?",
# # #                 "short_answer": "Judge the effectiveness of the main points.",
# # #                 "true_false": "The evidence strongly supports the conclusion.",
# # #                 "fill_blanks": "The strongest evidence is ___ because ___.",
# # #                 "medium_answer": "Assess the quality of the arguments presented.",
# # #                 "long_answer": "Critique the document's reasoning and evidence.",
# # #                 "matching": "Evaluate each claim against its supporting evidence."
# # #             },
# # #             "creating": {
# # #                 "multiple_choice": "What new solution could you develop?",
# # #                 "short_answer": "Design a new approach using these principles.",
# # #                 "true_false": "These concepts could be combined innovatively.",
# # #                 "fill_blanks": "A new innovation might combine ___ with ___.",
# # #                 "medium_answer": "Propose improvements to the existing ideas.",
# # #                 "long_answer": "Synthesize the concepts into a comprehensive framework.",
# # #                 "matching": "Create new connections between different elements."
# # #             }
# # #         }
        
# # #         # Generate questions
# # #         for bloom_level in bloom_levels:
# # #             for question_type in question_types:
# # #                 for i in range(num_questions):
# # #                     # Get template
# # #                     template = templates.get(bloom_level, {}).get(question_type, 
# # #                         f"Sample {bloom_level} {question_type} question about the content.")
                    
# # #                     # Create options for multiple choice
# # #                     options = []
# # #                     answer = f"Sample answer for this {bloom_level} level question."
                    
# # #                     if question_type == "multiple_choice":
# # #                         if bloom_level == "remembering":
# # #                             options = [
# # #                                 "The document's primary subject matter",
# # #                                 "A secondary topic mentioned briefly", 
# # #                                 "An unrelated concept",
# # #                                 "A minor detail from the conclusion"
# # #                             ]
# # #                             answer = "The document's primary subject matter"
# # #                         elif bloom_level == "understanding":
# # #                             options = [
# # #                                 "It represents a fundamental principle",
# # #                                 "It's a contradictory statement",
# # #                                 "It's an unimportant detail",
# # #                                 "It's a typing error"
# # #                             ]
# # #                             answer = "It represents a fundamental principle"
# # #                         else:
# # #                             options = [
# # #                                 f"Option A for {bloom_level}",
# # #                                 f"Option B for {bloom_level}",
# # #                                 f"Option C for {bloom_level}",
# # #                                 f"Option D for {bloom_level}"
# # #                             ]
# # #                             answer = f"Option A for {bloom_level}"
                    
# # #                     elif question_type == "true_false":
# # #                         answer = "True"
                    
# # #                     # Create question object
# # #                     question = {
# # #                         "id": str(uuid.uuid4()),
# # #                         "question_text": f"{template} (Question {i+1})",
# # #                         "question_type": question_type,
# # #                         "bloom_level": bloom_level,
# # #                         "difficulty": difficulty,
# # #                         "answer": answer,
# # #                         "options": options,
# # #                         "explanation": f"This {difficulty} question tests {bloom_level} level thinking by requiring students to {self._get_skill_description(bloom_level)}."
# # #                     }
# # #                     questions.append(question)
        
# # #         return questions
    
# # #     def _get_skill_description(self, bloom_level):
# # #         """Get description of cognitive skills for each Bloom level"""
# # #         skills = {
# # #             "remembering": "recall and recognize specific information",
# # #             "understanding": "comprehend and explain concepts in their own words",
# # #             "applying": "use knowledge and skills in new situations",
# # #             "analyzing": "break down information and examine relationships",
# # #             "evaluating": "make judgments and assess the value of ideas",
# # #             "creating": "synthesize information to generate new ideas or solutions"
# # #         }
# # #         return skills.get(bloom_level, "engage with the content meaningfully")

# # # class LLMProviderFactory:
# # #     """Factory class to create LLM providers"""
    
# # #     @staticmethod
# # #     def create_provider(provider_name: str) -> LLMProvider:
# # #         """Create an LLM provider - currently returns MockProvider for all types"""
# # #         # For now, always return MockProvider regardless of requested provider
# # #         # This ensures no external API dependencies
# # #         return MockProvider()

# # # core/llm_providers.py - Replace the entire file with this
# # import uuid
# # import json
# # import random
# # import re
# # from typing import List, Dict, Any
# # from django.conf import settings

# # # Try to import OpenAI, fall back to mock if not available
# # try:
# #     import openai
# #     OPENAI_AVAILABLE = bool(settings.OPENAI_API_KEY)
# # except ImportError:
# #     OPENAI_AVAILABLE = False

# # class LLMProvider:
# #     """Base class for LLM providers"""
# #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         raise NotImplementedError

# # class OpenAIProvider(LLMProvider):
# #     """Real OpenAI provider for question generation"""
    
# #     def __init__(self):
# #         if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
# #             self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
# #             self.use_openai = True
# #             print("✅ OpenAI client initialized successfully")
# #         else:
# #             self.use_openai = False
# #             print("⚠️ OpenAI not available, using enhanced mock")
    
# #     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         """Generate questions using OpenAI or enhanced mock"""
        
# #         if self.use_openai:
# #             return self._generate_with_openai(content, request_params)
# #         else:
# #             return self._generate_enhanced_mock(content, request_params)
    
# #     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         """Generate questions using OpenAI GPT"""
# #         bloom_levels = request_params.get("bloom_levels", ["remembering"])
# #         question_types = request_params.get("question_types", ["multiple_choice"])
# #         difficulty = request_params.get("difficulty", "medium")
# #         num_questions = request_params.get("num_questions_per_type", 2)
# #         language = request_params.get("language", "en")
        
# #         all_questions = []
        
# #         for bloom_level in bloom_levels:
# #             for question_type in question_types:
# #                 try:
# #                     # Generate questions for this bloom level and type
# #                     questions = self._call_openai_for_questions(
# #                         content, bloom_level, question_type, difficulty, language, num_questions
# #                     )
# #                     all_questions.extend(questions)
# #                 except Exception as e:
# #                     print(f"OpenAI error for {bloom_level}-{question_type}: {e}")
# #                     # Fall back to mock for this batch
# #                     fallback_questions = self._generate_fallback_questions(
# #                         content, bloom_level, question_type, difficulty, num_questions
# #                     )
# #                     all_questions.extend(fallback_questions)
        
# #         return all_questions
    
# #     def _call_openai_for_questions(self, content: str, bloom_level: str, question_type: str, 
# #                                   difficulty: str, language: str, num_questions: int) -> List[Dict[str, Any]]:
# #         """Make actual OpenAI API call"""
        
# #         # Prepare the prompt
# #         prompt = self._create_openai_prompt(content, bloom_level, question_type, difficulty, language, num_questions)
        
# #         try:
# #             response = self.client.chat.completions.create(
# #                 model="gpt-4o-mini",  # Using the model specified in your original code
# #                 messages=[
# #                     {
# #                         "role": "system", 
# #                         "content": "You are an expert educator skilled in creating high-quality educational questions based on Bloom's Taxonomy. Always respond with valid JSON format."
# #                     },
# #                     {
# #                         "role": "user", 
# #                         "content": prompt
# #                     }
# #                 ],
# #                 temperature=0.7,
# #                 max_tokens=2000,
# #                 response_format={"type": "json_object"}
# #             )
            
# #             response_text = response.choices[0].message.content
            
# #             # Parse the JSON response
# #             questions_data = json.loads(response_text)
            
# #             # Convert to our format
# #             questions = []
# #             for i, q_data in enumerate(questions_data.get("questions", []), 1):
# #                 question = {
# #                     "id": str(uuid.uuid4()),
# #                     "question_text": f"Question {i}: {q_data.get('question', 'Generated question')}",
# #                     "question_type": question_type,
# #                     "bloom_level": bloom_level,
# #                     "difficulty": difficulty,
# #                     "answer": q_data.get("answer", "Generated answer"),
# #                     "options": q_data.get("options", []),
# #                     "explanation": q_data.get("explanation", "Generated explanation"),
# #                     "topic": q_data.get("topic", ""),
# #                     "language": language
# #                 }
# #                 questions.append(question)
            
# #             return questions
            
# #         except json.JSONDecodeError as e:
# #             print(f"JSON parsing error: {e}")
# #             return self._generate_fallback_questions(content, bloom_level, question_type, difficulty, num_questions)
# #         except Exception as e:
# #             print(f"OpenAI API error: {e}")
# #             return self._generate_fallback_questions(content, bloom_level, question_type, difficulty, num_questions)
    
# #     def _create_openai_prompt(self, content: str, bloom_level: str, question_type: str, 
# #                              difficulty: str, language: str, num_questions: int) -> str:
# #         """Create a detailed prompt for OpenAI"""
        
# #         # Bloom level descriptions
# #         bloom_descriptions = {
# #             "remembering": "recall facts, terms, basic concepts, or answers from the content",
# #             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting concepts",
# #             "applying": "use information in new situations, solve problems using required skills or knowledge",
# #             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
# #             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
# #             "creating": "produce new or original work, reorganize elements into new patterns or structures"
# #         }
        
# #         # Question type instructions
# #         type_instructions = {
# #             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Provide the correct answer.",
# #             "short_answer": f"Create {num_questions} short answer questions expecting 1-2 sentence responses.",
# #             "medium_answer": f"Create {num_questions} medium answer questions expecting paragraph-length responses.",
# #             "long_answer": f"Create {num_questions} long answer questions expecting essay-style responses.",
# #             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
# #             "true_false": f"Create {num_questions} true/false questions with clear explanations.",
# #             "matching": f"Create {num_questions} matching questions with terms and definitions."
# #         }
        
# #         # Limit content length for API
# #         content_sample = content[:3000] if len(content) > 3000 else content
        
# #         prompt = f"""
# # Based on the following document content, create {num_questions} educational questions at the "{bloom_level}" level of Bloom's Taxonomy.

# # **REQUIREMENTS:**
# # - Bloom's Level: {bloom_level.title()} - {bloom_descriptions.get(bloom_level, '')}
# # - Question Type: {question_type}
# # - Difficulty: {difficulty}
# # - Language: {language}
# # - Number of questions: {num_questions}

# # **INSTRUCTIONS:**
# # {type_instructions.get(question_type, '')}

# # **CONTENT TO ANALYZE:**
# # {content_sample}

# # **OUTPUT FORMAT:**
# # Respond with valid JSON in this exact format:
# # {{
# #     "questions": [
# #         {{
# #             "question": "Your question text here",
# #             "answer": "The correct answer",
# #             "options": ["Option A", "Option B", "Option C", "Option D"],
# #             "explanation": "Why this answer is correct and how it relates to the {bloom_level} level",
# #             "topic": "Main topic/concept addressed"
# #         }}
# #     ]
# # }}

# # **IMPORTANT:**
# # - Questions must be directly based on the provided content
# # - For multiple choice, provide exactly 4 options
# # - For other types, options array can be empty
# # - Ensure questions test {bloom_level} level cognitive skills
# # - Make questions {difficulty} difficulty level
# # - Provide clear, educational explanations
# # """
        
# #         return prompt
    
# #     def _generate_fallback_questions(self, content: str, bloom_level: str, question_type: str, 
# #                                    difficulty: str, num_questions: int) -> List[Dict[str, Any]]:
# #         """Generate fallback questions when OpenAI fails"""
# #         questions = []
        
# #         # Extract key terms from content
# #         content_preview = content[:1000]
# #         key_terms = self._extract_key_terms(content_preview)
# #         main_topic = key_terms[0] if key_terms else "the main concept"
        
# #         for i in range(num_questions):
# #             question = {
# #                 "id": str(uuid.uuid4()),
# #                 "question_text": f"Question {i+1}: {self._get_fallback_question_text(bloom_level, question_type, main_topic)}",
# #                 "question_type": question_type,
# #                 "bloom_level": bloom_level,
# #                 "difficulty": difficulty,
# #                 "answer": f"Based on the document, {main_topic} is discussed as a key concept.",
# #                 "options": self._get_fallback_options(question_type, main_topic),
# #                 "explanation": f"This {difficulty} question tests {bloom_level} level thinking about {main_topic}.",
# #                 "topic": main_topic,
# #                 "language": "en"
# #             }
# #             questions.append(question)
        
# #         return questions
    
# #     def _extract_key_terms(self, content: str) -> List[str]:
# #         """Extract key terms from content"""
# #         # Simple keyword extraction
# #         words = re.findall(r'\b[A-Za-z]{4,}\b', content)
# #         common_words = {'that', 'this', 'with', 'from', 'they', 'been', 'have', 'were', 'said', 'each', 'which', 'their', 'time', 'will', 'about', 'would', 'there', 'could', 'other', 'more', 'very', 'what', 'know', 'just', 'first', 'into', 'over', 'think', 'also', 'your', 'work', 'life', 'only'}
        
# #         filtered_words = [word for word in words if word.lower() not in common_words]
# #         unique_terms = list(set(filtered_words))[:5]
        
# #         return unique_terms if unique_terms else ["main concept"]
    
# #     def _get_fallback_question_text(self, bloom_level: str, question_type: str, main_topic: str) -> str:
# #         """Generate fallback question text based on bloom level"""
# #         templates = {
# #             "remembering": {
# #                 "multiple_choice": f"What does the document say about {main_topic}?",
# #                 "short_answer": f"Define {main_topic} as presented in the document.",
# #                 "fill_blanks": f"The document discusses ___ as a key aspect of {main_topic}.",
# #                 "true_false": f"The document provides detailed information about {main_topic}."
# #             },
# #             "understanding": {
# #                 "multiple_choice": f"How does the document explain the significance of {main_topic}?",
# #                 "short_answer": f"Explain the main points about {main_topic} from the document.",
# #                 "fill_blanks": f"According to the document, {main_topic} is important because ___."
# #             },
# #             "applying": {
# #                 "multiple_choice": f"How could the concepts related to {main_topic} be applied in practice?",
# #                 "short_answer": f"Describe how you would use the information about {main_topic}."
# #             },
# #             "analyzing": {
# #                 "multiple_choice": f"What are the key components of {main_topic} discussed in the document?",
# #                 "short_answer": f"Analyze the relationship between {main_topic} and other concepts."
# #             },
# #             "evaluating": {
# #                 "multiple_choice": f"What is the most important aspect of {main_topic} according to the document?",
# #                 "short_answer": f"Evaluate the significance of {main_topic} based on the document."
# #             },
# #             "creating": {
# #                 "multiple_choice": f"How could you combine {main_topic} with other concepts to create something new?",
# #                 "short_answer": f"Design a new approach using the principles of {main_topic}."
# #             }
# #         }
        
# #         return templates.get(bloom_level, {}).get(question_type, f"What is discussed about {main_topic} in the document?")
    
# #     def _get_fallback_options(self, question_type: str, main_topic: str) -> List[str]:
# #         """Generate fallback options for multiple choice"""
# #         if question_type == "multiple_choice":
# #             return [
# #                 f"The document emphasizes {main_topic} as important",
# #                 f"The document briefly mentions {main_topic}",
# #                 f"The document contradicts the importance of {main_topic}",
# #                 f"The document does not discuss {main_topic}"
# #             ]
# #         return []
    
# #     def _generate_enhanced_mock(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
# #         """Enhanced mock generation when OpenAI is not available"""
# #         # This is a fallback when OpenAI is completely unavailable
# #         # Use the improved mock logic from before
# #         return self._generate_fallback_questions(
# #             content, 
# #             request_params.get("bloom_levels", ["remembering"])[0],
# #             request_params.get("question_types", ["multiple_choice"])[0],
# #             request_params.get("difficulty", "medium"),
# #             request_params.get("num_questions_per_type", 2)
# #         )

# # class LLMProviderFactory:
# #     """Factory class to create LLM providers"""
    
# #     @staticmethod
# #     def create_provider(provider_name: str) -> LLMProvider:
# #         """Create an LLM provider"""
# #         if provider_name in ["openai", "anthropic", "deepseek", "gemini"]:
# #             return OpenAIProvider()  # All use OpenAI provider for now
# #         else:
# #             return OpenAIProvider()  # Default to OpenAI





# # core/llm_providers.py - Complete Updated File
# import uuid
# import json
# import random
# import re
# from typing import List, Dict, Any
# from django.conf import settings

# # Try to import OpenAI, fall back to mock if not available
# try:
#     import openai
#     OPENAI_AVAILABLE = bool(settings.OPENAI_API_KEY)
# except ImportError:
#     OPENAI_AVAILABLE = False

# class LLMProvider:
#     """Base class for LLM providers"""
#     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         raise NotImplementedError

# class OpenAIProvider(LLMProvider):
#     """Real OpenAI provider for question generation"""
    
#     def __init__(self):
#         self.use_openai = False
#         self.client = None
        
#         # Check if OpenAI is available and API key is configured
#         if OPENAI_AVAILABLE and settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
#             try:
#                 self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
#                 # Test the connection with a simple call
#                 test_response = self.client.chat.completions.create(
#                     model="gpt-4o-mini",
#                     messages=[{"role": "user", "content": "test"}],
#                     max_tokens=5
#                 )
#                 self.use_openai = True
#                 print("✅ OpenAI client initialized and tested successfully")
#             except Exception as e:
#                 print(f"❌ OpenAI initialization failed: {e}")
#                 self.use_openai = False
#         else:
#             print("❌ OpenAI not available - missing API key or import failed")
#             self.use_openai = False
    
#     def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Generate questions using OpenAI or enhanced mock"""
        
#         # Always try OpenAI first if available
#         if self.use_openai and self.client:
#             try:
#                 print("🚀 Using OpenAI for question generation...")
#                 return self._generate_with_openai(content, request_params)
#             except Exception as e:
#                 print(f"❌ OpenAI generation failed: {e}")
#                 print("⚠️ Falling back to enhanced mock generation...")
#         else:
#             print("⚠️ Using enhanced mock generation - OpenAI not available")
        
#         return self._generate_enhanced_mock(content, request_params)
    
#     def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Generate questions using OpenAI GPT"""
#         bloom_levels = request_params.get("bloom_levels", ["remembering"])
#         question_types = request_params.get("question_types", ["multiple_choice"])
#         difficulty = request_params.get("difficulty", "medium")
#         num_questions = request_params.get("num_questions_per_type", 2)
#         language = request_params.get("language", "en")
        
#         all_questions = []
        
#         for bloom_level in bloom_levels:
#             for question_type in question_types:
#                 try:
#                     questions = self._call_openai_for_questions(
#                         content, bloom_level, question_type, difficulty, language, num_questions
#                     )
#                     all_questions.extend(questions)
#                 except Exception as e:
#                     print(f"OpenAI error for {bloom_level}-{question_type}: {e}")
#                     # Create fallback questions based on actual content
#                     fallback_questions = self._generate_content_based_fallback(
#                         content, bloom_level, question_type, difficulty, language, num_questions
#                     )
#                     all_questions.extend(fallback_questions)
        
#         return all_questions
    
#     def _call_openai_for_questions(self, content: str, bloom_level: str, question_type: str, 
#                                   difficulty: str, language: str, num_questions: int) -> List[Dict[str, Any]]:
#         """Make actual OpenAI API call"""
        
#         prompt = self._create_openai_prompt(content, bloom_level, question_type, difficulty, language, num_questions)
        
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                     {
#                         "role": "system", 
#                         "content": f"You are an expert educator creating questions in {language} language. Always respond with valid JSON format."
#                     },
#                     {
#                         "role": "user", 
#                         "content": prompt
#                     }
#                 ],
#                 temperature=0.7,
#                 max_tokens=2000,
#                 response_format={"type": "json_object"}
#             )
            
#             response_text = response.choices[0].message.content
#             questions_data = json.loads(response_text)
            
#             # Convert to our format
#             questions = []
#             for i, q_data in enumerate(questions_data.get("questions", []), 1):
#                 question = {
#                     "id": str(uuid.uuid4()),
#                     "question_text": f"Question {i}: {q_data.get('question', 'Generated question')}",
#                     "question_type": question_type,
#                     "bloom_level": bloom_level,
#                     "difficulty": difficulty,
#                     "answer": q_data.get("answer", "Generated answer"),
#                     "options": q_data.get("options", []),
#                     "explanation": q_data.get("explanation", "Generated explanation"),
#                     "topic": q_data.get("topic", ""),
#                     "language": language
#                 }
#                 questions.append(question)
            
#             return questions
            
#         except json.JSONDecodeError as e:
#             print(f"JSON parsing error: {e}")
#             return self._generate_content_based_fallback(content, bloom_level, question_type, difficulty, language, num_questions)
#         except Exception as e:
#             print(f"OpenAI API error: {e}")
#             return self._generate_content_based_fallback(content, bloom_level, question_type, difficulty, language, num_questions)
    
#     def _create_openai_prompt(self, content: str, bloom_level: str, question_type: str, 
#                              difficulty: str, language: str, num_questions: int) -> str:
#         """Create a detailed prompt for OpenAI"""
        
#         # Bloom level descriptions
#         bloom_descriptions = {
#             "remembering": "recall facts, terms, basic concepts, or answers from the content",
#             "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting concepts",
#             "applying": "use information in new situations, solve problems using required skills or knowledge",
#             "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
#             "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
#             "creating": "produce new or original work, reorganize elements into new patterns or structures"
#         }
        
#         # Language-specific instructions
#         language_instructions = {
#             'hi': "Create questions in Hindi language using Devanagari script. Base questions on the Hindi content provided.",
#             'te': "Create questions in Telugu language using Telugu script. Base questions on the Telugu content provided.",
#             'ur': "Create questions in Urdu language using Arabic script. Base questions on the Urdu content provided.",
#             'ar': "Create questions in Arabic language using Arabic script. Base questions on the Arabic content provided.",
#             'en': "Create questions in English language. Base questions on the English content provided."
#         }
        
#         # Question type instructions
#         type_instructions = {
#             "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Provide the correct answer.",
#             "short_answer": f"Create {num_questions} short answer questions expecting 1-2 sentence responses.",
#             "medium_answer": f"Create {num_questions} medium answer questions expecting paragraph-length responses.",
#             "long_answer": f"Create {num_questions} long answer questions expecting essay-style responses.",
#             "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
#             "true_false": f"Create {num_questions} true/false questions with clear explanations.",
#             "matching": f"Create {num_questions} matching questions with terms and definitions."
#         }
        
#         # Limit content length for API
#         content_sample = content[:4000] if len(content) > 4000 else content
        
#         prompt = f"""
# Based on the following document content, create {num_questions} educational questions at the "{bloom_level}" level of Bloom's Taxonomy.

# **REQUIREMENTS:**
# - Bloom's Level: {bloom_level.title()} - {bloom_descriptions.get(bloom_level, '')}
# - Question Type: {question_type}
# - Difficulty: {difficulty}
# - Language: {language}
# - Number of questions: {num_questions}

# **LANGUAGE INSTRUCTIONS:**
# {language_instructions.get(language, language_instructions['en'])}

# **QUESTION TYPE INSTRUCTIONS:**
# {type_instructions.get(question_type, '')}

# **DOCUMENT CONTENT TO ANALYZE:**
# {content_sample}

# **OUTPUT FORMAT:**
# Respond with valid JSON in this exact format:
# {{
#     "questions": [
#         {{
#             "question": "Your question text here in {language}",
#             "answer": "The correct answer in {language}",
#             "options": ["Option A", "Option B", "Option C", "Option D"],
#             "explanation": "Why this answer is correct and how it relates to the {bloom_level} level in {language}",
#             "topic": "Main topic/concept addressed"
#         }}
#     ]
# }}

# **IMPORTANT:**
# - Questions must be directly based on the provided document content
# - For multiple choice, provide exactly 4 options in the specified language
# - For other types, options array can be empty
# - Ensure questions test {bloom_level} level cognitive skills
# - Make questions {difficulty} difficulty level
# - All text must be in {language} language
# - Extract real concepts, names, and facts from the document content
# - Do not use placeholder text like "main concept" - use actual content from the document
# """
        
#         return prompt
    
#     def _generate_content_based_fallback(self, content: str, bloom_level: str, question_type: str, 
#                                        difficulty: str, language: str, num_questions: int) -> List[Dict[str, Any]]:
#         """Generate fallback questions based on actual content analysis"""
#         questions = []
        
#         # Extract key information from content
#         content_info = self._analyze_content(content, language)
        
#         for i in range(num_questions):
#             question_text = self._generate_question_text(content_info, bloom_level, question_type, language, i+1)
#             answer = self._generate_answer_text(content_info, bloom_level, language)
#             options = self._generate_options(content_info, question_type, language)
#             explanation = self._generate_explanation(content_info, bloom_level, language)
            
#             question = {
#                 "id": str(uuid.uuid4()),
#                 "question_text": question_text,
#                 "question_type": question_type,
#                 "bloom_level": bloom_level,
#                 "difficulty": difficulty,
#                 "answer": answer,
#                 "options": options,
#                 "explanation": explanation,
#                 "topic": content_info.get('main_topic', 'Document content'),
#                 "language": language
#             }
#             questions.append(question)
        
#         return questions
    
#     def _analyze_content(self, content: str, language: str) -> Dict[str, Any]:
#         """Analyze content to extract key information"""
#         # Basic content analysis
#         words = content.split()
#         sentences = re.split(r'[।\.\!\?]', content)
        
#         # Extract potential names, dates, places
#         names = re.findall(r'[A-Z][a-z]+', content) if language == 'en' else []
#         dates = re.findall(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}|\d{4}', content)
        
#         # For Hindi content, extract Hindi words
#         if language == 'hi':
#             hindi_words = re.findall(r'[\u0900-\u097F]+', content)
#             names.extend(hindi_words[:5])  # Take first 5 Hindi words as potential names/concepts
        
#         # For Telugu content
#         elif language == 'te':
#             telugu_words = re.findall(r'[\u0C00-\u0C7F]+', content)
#             names.extend(telugu_words[:5])
        
#         # For Urdu content
#         elif language == 'ur':
#             urdu_words = re.findall(r'[\u0600-\u06FF]+', content)
#             names.extend(urdu_words[:5])
        
#         return {
#             'main_topic': names[0] if names else 'document content',
#             'key_concepts': names[:3] if names else ['concept 1', 'concept 2', 'concept 3'],
#             'dates': dates[:2] if dates else [],
#             'first_sentence': sentences[0].strip() if sentences else content[:100],
#             'word_count': len(words),
#             'language': language
#         }
    
#     def _generate_question_text(self, content_info: dict, bloom_level: str, question_type: str, language: str, question_num: int) -> str:
#         """Generate question text based on content analysis"""
#         main_topic = content_info['main_topic']
#         concepts = content_info['key_concepts']
        
#         templates = {
#             'en': {
#                 'remembering': {
#                     'multiple_choice': f"What information is provided about {main_topic} in the document?",
#                     'short_answer': f"Who is {main_topic} according to the document?",
#                     'true_false': f"The document discusses {main_topic} in detail."
#                 },
#                 'understanding': {
#                     'multiple_choice': f"What is the significance of {main_topic} based on the document?",
#                     'short_answer': f"Explain the main points about {main_topic} mentioned in the document."
#                 }
#             },
#             'hi': {
#                 'remembering': {
#                     'multiple_choice': f"दस्तावेज़ में {main_topic} के बारे में क्या जानकारी दी गई है?",
#                     'short_answer': f"दस्तावेज़ के अनुसार {main_topic} कौन हैं?",
#                     'true_false': f"दस्तावेज़ में {main_topic} की विस्तार से चर्चा की गई है।"
#                 },
#                 'understanding': {
#                     'multiple_choice': f"दस्तावेज़ के आधार पर {main_topic} का क्या महत्व है?",
#                     'short_answer': f"दस्तावेज़ में उल्लिखित {main_topic} के मुख्य बिंदुओं की व्याख्या करें।"
#                 }
#             },
#             'te': {
#                 'remembering': {
#                     'multiple_choice': f"పత్రంలో {main_topic} గురించి ఎలాంటి సమాచారం ఇవ్వబడింది?",
#                     'short_answer': f"పత్రం ప్రకారం {main_topic} ఎవరు?",
#                     'true_false': f"పత్రంలో {main_topic} గురించి వివరంగా చర్చించబడింది।"
#                 }
#             },
#             'ur': {
#                 'remembering': {
#                     'multiple_choice': f"دستاویز میں {main_topic} کے بارے میں کیا معلومات دی گئی ہیں؟",
#                     'short_answer': f"دستاویز کے مطابق {main_topic} کون ہیں؟",
#                     'true_false': f"دستاویز میں {main_topic} کی تفصیل سے بحث کی گئی ہے۔"
#                 }
#             }
#         }
        
#         lang_templates = templates.get(language, templates['en'])
#         bloom_templates = lang_templates.get(bloom_level, lang_templates.get('remembering', {}))
#         template = bloom_templates.get(question_type, f"Question about {main_topic}")
        
#         return f"प्रश्न {question_num}: {template}" if language == 'hi' else f"Question {question_num}: {template}"
    
#     def _generate_answer_text(self, content_info: dict, bloom_level: str, language: str) -> str:
#         """Generate answer based on content"""
#         main_topic = content_info['main_topic']
        
#         answers = {
#             'en': f"Based on the document, {main_topic} is discussed as a key figure/concept with specific details provided.",
#             'hi': f"दस्तावेज़ के अनुसार, {main_topic} एक महत्वपूर्ण व्यक्ति/अवधारणा के रूप में चर्चित हैं।",
#             'te': f"పత్రం ప్రకారం, {main_topic} ఒక ముఖ్యమైన వ్యక్తి/భావనగా చర్చించబడింది।",
#             'ur': f"دستاویز کے مطابق، {main_topic} ایک اہم شخصیت/تصور کے طور پر زیر بحث ہے۔"
#         }
        
#         return answers.get(language, answers['en'])
    
#     def _generate_options(self, content_info: dict, question_type: str, language: str) -> List[str]:
#         """Generate options for multiple choice questions"""
#         if question_type != "multiple_choice":
#             return []
        
#         main_topic = content_info['main_topic']
        
#         options_templates = {
#             'en': [
#                 f"Information about {main_topic} is provided",
#                 f"No information about {main_topic} is given",
#                 f"Only brief mention of {main_topic}",
#                 f"Contradictory information about {main_topic}"
#             ],
#             'hi': [
#                 f"{main_topic} के बारे में जानकारी दी गई है",
#                 f"{main_topic} के बारे में कोई जानकारी नहीं दी गई",
#                 f"{main_topic} का केवल संक्षिप्त उल्लेख",
#                 f"{main_topic} के बारे में विरोधाभासी जानकारी"
#             ],
#             'te': [
#                 f"{main_topic} గురించి సమాచారం ఇవ్వబడింది",
#                 f"{main_topic} గురించి ఎలాంటి సమాచారం లేదు",
#                 f"{main_topic} గురించి కేవలం క్లుప్త ప్రస్తావన",
#                 f"{main_topic} గురించి వైరుధ్య సమాచారం"
#             ],
#             'ur': [
#                 f"{main_topic} کے بارے میں معلومات دی گئی ہیں",
#                 f"{main_topic} کے بارے میں کوئی معلومات نہیں",
#                 f"{main_topic} کا صرف مختصر ذکر",
#                 f"{main_topic} کے بارے میں متضاد معلومات"
#             ]
#         }
        
#         options = options_templates.get(language, options_templates['en'])
#         random.shuffle(options)
#         return options
    
#     def _generate_explanation(self, content_info: dict, bloom_level: str, language: str) -> str:
#         """Generate explanation for the answer"""
#         explanations = {
#             'en': f"This question tests {bloom_level} level understanding by asking about specific content from the document.",
#             'hi': f"यह प्रश्न दस्तावेज़ की विशिष्ट सामग्री के बारे में पूछकर {bloom_level} स्तर की समझ का परीक्षण करता है।",
#             'te': f"ఈ ప్రశ్న పత్రంలోని నిర్దిష్ట కంటెంట్ గురించి అడగడం ద్వారా {bloom_level} స్థాయి అవగాహనను పరీక్షిస్తుంది।",
#             'ur': f"یہ سوال دستاویز کے مخصوص مواد کے بارے میں پوچھ کر {bloom_level} سطح کی سمجھ کو آزماتا ہے۔"
#         }
        
#         return explanations.get(language, explanations['en'])
    
#     def _generate_enhanced_mock(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """Enhanced mock generation when OpenAI is not available"""
#         bloom_levels = request_params.get("bloom_levels", ["remembering"])
#         question_types = request_params.get("question_types", ["multiple_choice"])
#         difficulty = request_params.get("difficulty", "medium")
#         num_questions = request_params.get("num_questions_per_type", 2)
#         language = request_params.get("language", "en")
        
#         all_questions = []
        
#         for bloom_level in bloom_levels:
#             for question_type in question_types:
#                 questions = self._generate_content_based_fallback(
#                     content, bloom_level, question_type, difficulty, language, num_questions
#                 )
#                 all_questions.extend(questions)
        
#         return all_questions

# class LLMProviderFactory:
#     """Factory class to create LLM providers"""
    
#     @staticmethod
#     def create_provider(provider_name: str) -> LLMProvider:
#         """Create an LLM provider"""
#         # For now, always return OpenAI provider which handles fallback internally
#         return OpenAIProvider()


# core/llm_providers.py
import uuid
import json
import random
import re
from typing import List, Dict, Any
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Try to import OpenAI
try:
    import openai
    OPENAI_AVAILABLE = bool(settings.OPENAI_API_KEY)
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI module not installed")

class LLMProvider:
    """Base class for LLM providers"""
    def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """Real OpenAI provider for question generation"""
    
    def __init__(self):
        self.use_openai = False
        if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
            try:
                self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                self.use_openai = True
                logger.info("✅ OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.use_openai = False
        else:
            logger.warning("⚠️ OpenAI not available, using enhanced content-based generation")
    
    def generate_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions using OpenAI or content-based generation"""
        
        if self.use_openai:
            try:
                return self._generate_with_openai(content, request_params)
            except Exception as e:
                logger.error(f"OpenAI generation failed: {e}, falling back to content-based")
                return self._generate_content_based_questions(content, request_params)
        else:
            return self._generate_content_based_questions(content, request_params)
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extract key concepts from content"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                      'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                      'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        
        # Filter out stop words and count frequency
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and get top concepts
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        key_concepts = [word[0] for word in sorted_words[:10]]
        
        return key_concepts
    
    def _extract_sentences(self, content: str) -> List[str]:
        """Extract meaningful sentences from content"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        
        # Filter meaningful sentences (more than 5 words)
        meaningful_sentences = []
        for sentence in sentences:
            words = sentence.strip().split()
            if len(words) > 5:
                meaningful_sentences.append(sentence.strip())
        
        return meaningful_sentences[:20]  # Limit to first 20 sentences
    
    def _generate_content_based_questions(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions based on actual content analysis"""
        
        bloom_levels = request_params.get("bloom_levels", ["remembering"])
        question_types = request_params.get("question_types", ["multiple_choice"])
        difficulty = request_params.get("difficulty", "medium")
        num_questions = request_params.get("num_questions_per_type", 2)
        language = request_params.get("language", "en")
        
        # Extract key concepts and sentences
        key_concepts = self._extract_key_concepts(content)
        sentences = self._extract_sentences(content)
        
        if not key_concepts:
            key_concepts = ["main topic", "key concept", "important idea"]
        
        if not sentences:
            sentences = [content[:200] + "..."]
        
        all_questions = []
        question_number = 1
        
        for bloom_level in bloom_levels:
            for question_type in question_types:
                for i in range(num_questions):
                    # Select a random concept and sentence
                    concept = random.choice(key_concepts)
                    sentence = random.choice(sentences)
                    
                    # Generate question based on bloom level
                    question_data = self._create_question_for_bloom_level(
                        concept, sentence, bloom_level, question_type, 
                        difficulty, question_number, content
                    )
                    
                    all_questions.append(question_data)
                    question_number += 1
        
        return all_questions
    
    def _create_question_for_bloom_level(self, concept: str, sentence: str, bloom_level: str, 
                                       question_type: str, difficulty: str, question_number: int,
                                       full_content: str) -> Dict[str, Any]:
        """Create a question based on bloom level and actual content"""
        
        # Question templates based on bloom level
        templates = {
            'remembering': {
                'multiple_choice': f"According to the document, what is {concept}?",
                'short_answer': f"Define {concept} as mentioned in the document.",
                'true_false': f"The document discusses {concept}.",
                'fill_blanks': f"Based on the document, {concept} is defined as ___."
            },
            'understanding': {
                'multiple_choice': f"What does the document say about the significance of {concept}?",
                'short_answer': f"Explain the main idea related to {concept} from the document.",
                'true_false': f"The document suggests that {concept} is important.",
                'fill_blanks': f"The document explains that {concept} is important because ___."
            },
            'applying': {
                'multiple_choice': f"How would you apply the concept of {concept} discussed in the document?",
                'short_answer': f"Give an example of how {concept} could be used based on the document.",
                'true_false': f"The principles of {concept} can be applied in practice.",
                'fill_blanks': f"To apply {concept}, one would need to ___."
            },
            'analyzing': {
                'multiple_choice': f"What are the key components of {concept} according to the document?",
                'short_answer': f"Analyze the relationship between {concept} and other ideas in the document.",
                'true_false': f"The document presents multiple perspectives on {concept}.",
                'fill_blanks': f"The analysis shows that {concept} is related to ___ because ___."
            },
            'evaluating': {
                'multiple_choice': f"Based on the document, which aspect of {concept} is most significant?",
                'short_answer': f"Evaluate the importance of {concept} based on the document's arguments.",
                'true_false': f"The evidence in the document strongly supports the importance of {concept}.",
                'fill_blanks': f"The most compelling evidence about {concept} is ___."
            },
            'creating': {
                'multiple_choice': f"What new approach could be developed based on the document's discussion of {concept}?",
                'short_answer': f"Design a new solution using {concept} principles from the document.",
                'true_false': f"The concepts about {concept} could be combined to create new solutions.",
                'fill_blanks': f"A new innovation based on {concept} might involve ___."
            }
        }
        
        # Get the appropriate template
        bloom_templates = templates.get(bloom_level, templates['remembering'])
        question_text = bloom_templates.get(question_type, bloom_templates.get('multiple_choice'))
        
        # Add question number
        question_text = f"Question {question_number}: {question_text}"
        
        # Generate answer based on actual content
        answer = self._generate_answer_from_content(concept, sentence, bloom_level, full_content)
        
        # Generate options for multiple choice
        options = []
        if question_type == 'multiple_choice':
            options = self._generate_options_from_content(concept, answer, sentence, full_content)
        elif question_type == 'true_false':
            answer = random.choice(["True", "False"])
            options = ["True", "False"]
        
        # Generate explanation
        explanation = f"This question tests {bloom_level} level understanding of '{concept}'. "
        explanation += f"The answer is based on this excerpt: '{sentence[:100]}...'"
        
        return {
            "id": str(uuid.uuid4()),
            "question_text": question_text,
            "question_type": question_type,
            "bloom_level": bloom_level,
            "difficulty": difficulty,
            "answer": answer,
            "options": options,
            "explanation": explanation,
            "topic": concept,
            "language": "en"
        }
    
    def _generate_answer_from_content(self, concept: str, sentence: str, bloom_level: str, 
                                    full_content: str) -> str:
        """Generate answer based on actual content"""
        
        if bloom_level == 'remembering':
            # Find definition or description in content
            pattern = rf"{concept}[^.]*(?:is|are|means|refers to)[^.]*\."
            match = re.search(pattern, full_content, re.IGNORECASE)
            if match:
                return match.group(0).strip()
            else:
                return f"Based on the document, {concept} is mentioned in the context: {sentence[:150]}..."
        
        elif bloom_level == 'understanding':
            return f"The document explains that {concept} is significant because it {sentence[:100]}..."
        
        elif bloom_level == 'applying':
            return f"According to the document, {concept} can be applied by {sentence[:100]}..."
        
        elif bloom_level == 'analyzing':
            # Find relationships
            other_concepts = self._extract_key_concepts(full_content)
            other_concepts = [c for c in other_concepts if c != concept][:2]
            return f"The document shows that {concept} is related to {', '.join(other_concepts)} through {sentence[:80]}..."
        
        elif bloom_level == 'evaluating':
            return f"Based on the evidence in the document, {concept} is important because {sentence[:100]}..."
        
        else:  # creating
            return f"A new approach based on {concept} could involve combining it with the ideas discussed: {sentence[:80]}..."
    
    def _generate_options_from_content(self, concept: str, correct_answer: str, 
                                      sentence: str, full_content: str) -> List[str]:
        """Generate multiple choice options based on content"""
        
        options = [correct_answer]
        
        # Extract other concepts for wrong options
        other_concepts = self._extract_key_concepts(full_content)
        other_concepts = [c for c in other_concepts if c != concept]
        
        # Generate plausible but incorrect options
        wrong_patterns = [
            f"The document states that {concept} is unrelated to the main topic",
            f"According to the document, {concept} is not significant",
            f"The document defines {concept} as {random.choice(other_concepts) if other_concepts else 'something else'}",
            f"Based on the document, {concept} contradicts the main argument"
        ]
        
        # Add 3 wrong options
        random.shuffle(wrong_patterns)
        options.extend(wrong_patterns[:3])
        
        # Shuffle all options
        random.shuffle(options)
        
        return options
    
    def _generate_with_openai(self, content: str, request_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate questions using OpenAI GPT"""
        bloom_levels = request_params.get("bloom_levels", ["remembering"])
        question_types = request_params.get("question_types", ["multiple_choice"])
        difficulty = request_params.get("difficulty", "medium")
        num_questions = request_params.get("num_questions_per_type", 2)
        language = request_params.get("language", "en")
        
        all_questions = []
        
        for bloom_level in bloom_levels:
            for question_type in question_types:
                try:
                    # Generate questions for this bloom level and type
                    questions = self._call_openai_for_questions(
                        content, bloom_level, question_type, difficulty, language, num_questions
                    )
                    all_questions.extend(questions)
                except Exception as e:
                    logger.error(f"OpenAI error for {bloom_level}-{question_type}: {e}")
                    # Fall back to content-based generation for this batch
                    fallback_questions = self._generate_content_based_questions(
                        content, {
                            'bloom_levels': [bloom_level],
                            'question_types': [question_type],
                            'difficulty': difficulty,
                            'num_questions_per_type': num_questions,
                            'language': language
                        }
                    )
                    all_questions.extend(fallback_questions)
        
        return all_questions
    
    def _call_openai_for_questions(self, content: str, bloom_level: str, question_type: str, 
                                  difficulty: str, language: str, num_questions: int) -> List[Dict[str, Any]]:
        """Make actual OpenAI API call"""
        
        # Prepare the prompt
        prompt = self._create_openai_prompt(content, bloom_level, question_type, difficulty, language, num_questions)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert educator skilled in creating high-quality educational questions based on Bloom's Taxonomy. Always base your questions directly on the provided content."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(0)
                
                questions_data = json.loads(response_text)
                
                # Convert to our format
                questions = []
                for i, q_data in enumerate(questions_data.get("questions", []), 1):
                    question = {
                        "id": str(uuid.uuid4()),
                        "question_text": f"Question {i}: {q_data.get('question', 'Generated question')}",
                        "question_type": question_type,
                        "bloom_level": bloom_level,
                        "difficulty": difficulty,
                        "answer": q_data.get("answer", "Generated answer"),
                        "options": q_data.get("options", []),
                        "explanation": q_data.get("explanation", "Generated explanation"),
                        "topic": q_data.get("topic", ""),
                        "language": language
                    }
                    questions.append(question)
                
                return questions
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                # Fall back to content-based generation
                raise
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _create_openai_prompt(self, content: str, bloom_level: str, question_type: str, 
                             difficulty: str, language: str, num_questions: int) -> str:
        """Create a detailed prompt for OpenAI"""
        
        # Bloom level descriptions
        bloom_descriptions = {
            "remembering": "recall facts, terms, basic concepts, or answers from the content",
            "understanding": "demonstrate comprehension by organizing, comparing, translating, interpreting concepts",
            "applying": "use information in new situations, solve problems using required skills or knowledge",
            "analyzing": "draw connections among ideas, determine how parts relate to overall structure",
            "evaluating": "justify decisions or opinions, make judgments based on criteria and standards",
            "creating": "produce new or original work, reorganize elements into new patterns or structures"
        }
        
        # Question type instructions
        type_instructions = {
            "multiple_choice": f"Create {num_questions} multiple choice questions with 4 options (A, B, C, D). Provide the correct answer.",
            "short_answer": f"Create {num_questions} short answer questions expecting 1-2 sentence responses.",
            "medium_answer": f"Create {num_questions} medium answer questions expecting paragraph-length responses.",
            "long_answer": f"Create {num_questions} long answer questions expecting essay-style responses.",
            "fill_blanks": f"Create {num_questions} fill-in-the-blank questions with key terms removed.",
            "true_false": f"Create {num_questions} true/false questions with clear explanations.",
            "matching": f"Create {num_questions} matching questions with terms and definitions."
        }
        
        # Limit content length for API
        content_sample = content[:3000] if len(content) > 3000 else content
        
        prompt = f"""
Based on the following document content, create {num_questions} educational questions at the "{bloom_level}" level of Bloom's Taxonomy.

**IMPORTANT**: All questions MUST be based directly on the content provided. Do not ask about concepts not mentioned in the document.

**REQUIREMENTS:**
- Bloom's Level: {bloom_level.title()} - {bloom_descriptions.get(bloom_level, '')}
- Question Type: {question_type}
- Difficulty: {difficulty}
- Language: {language}
- Number of questions: {num_questions}

**INSTRUCTIONS:**
{type_instructions.get(question_type, '')}

**CONTENT TO ANALYZE:**
{content_sample}

**OUTPUT FORMAT:**
Respond with valid JSON in this exact format:
{{
    "questions": [
        {{
            "question": "Your question text here (must be based on the content above)",
            "answer": "The correct answer (must be found in or derived from the content)",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "explanation": "Why this answer is correct based on the content",
            "topic": "Main topic/concept addressed from the content"
        }}
    ]
}}

**CRITICAL RULES:**
1. Every question must reference specific information from the provided content
2. Answers must be verifiable from the content
3. Do not invent information not present in the content
4. For multiple choice, make all options plausible but only one correct
5. Ensure questions test {bloom_level} level cognitive skills
"""
        
        return prompt

class LLMProviderFactory:
    """Factory class to create LLM providers"""
    
    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        """Create an LLM provider"""
        return OpenAIProvider()