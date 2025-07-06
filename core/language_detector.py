# core/language_detector.py
import re
from langdetect import detect, DetectorFactory
from typing import Dict, Tuple

# Ensure consistent detection
DetectorFactory.seed = 0

class LanguageDetector:
    
    # Script patterns for Indian languages
    SCRIPT_PATTERNS = {
        'hi': r'[\u0900-\u097F]+',  # Devanagari (Hindi)
        'te': r'[\u0C00-\u0C7F]+',  # Telugu
        'ur': r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+',  # Arabic/Urdu
        'ar': r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+',  # Arabic
        'bn': r'[\u0980-\u09FF]+',  # Bengali
        'ta': r'[\u0B80-\u0BFF]+',  # Tamil
        'ml': r'[\u0D00-\u0D7F]+',  # Malayalam
        'kn': r'[\u0C80-\u0CFF]+',  # Kannada
        'gu': r'[\u0A80-\u0AFF]+',  # Gujarati
        'mr': r'[\u0900-\u097F]+',  # Marathi (Devanagari)
        'pa': r'[\u0A00-\u0A7F]+',  # Punjabi (Gurmukhi)
        'or': r'[\u0B00-\u0B7F]+',  # Odia
        'as': r'[\u0980-\u09FF]+',  # Assamese
    }
    
    # Language confidence thresholds
    CONFIDENCE_THRESHOLD = 0.8
    
    @classmethod
    def detect_language_advanced(cls, text: str) -> Dict[str, any]:
        """Advanced language detection with script analysis"""
        
        # Clean text for better detection
        clean_text = re.sub(r'[^\w\s]', ' ', text)
        sample_text = clean_text[:2000]  # Use first 2000 chars
        
        # Primary language detection
        try:
            primary_lang = detect(sample_text)
            confidence = 0.9  # langdetect doesn't provide confidence, assume high
        except:
            primary_lang = 'en'
            confidence = 0.5
        
        # Script-based detection for Indian languages
        detected_scripts = []
        script_counts = {}
        
        for lang_code, pattern in cls.SCRIPT_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                detected_scripts.append(lang_code)
                script_counts[lang_code] = len(''.join(matches))
        
        # If script detection found languages, use the most frequent one
        if script_counts:
            most_frequent_script = max(script_counts, key=script_counts.get)
            
            # If script detection contradicts langdetect, trust script for Indian languages
            if most_frequent_script != primary_lang and script_counts[most_frequent_script] > 50:
                primary_lang = most_frequent_script
                confidence = 0.95
        
        # Determine script type and reading direction
        script_info = cls.get_script_info(primary_lang)
        
        return {
            'language': primary_lang,
            'confidence': confidence,
            'detected_scripts': detected_scripts,
            'script_counts': script_counts,
            'script_type': script_info['script_type'],
            'reading_direction': script_info['reading_direction'],
            'font_family': script_info['font_family']
        }
    
    @classmethod
    def get_script_info(cls, language: str) -> Dict[str, str]:
        """Get script information for a language"""
        
        script_mapping = {
            'hi': {'script_type': 'devanagari', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Devanagari'},
            'mr': {'script_type': 'devanagari', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Devanagari'},
            'ne': {'script_type': 'devanagari', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Devanagari'},
            'te': {'script_type': 'telugu', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Telugu'},
            'ur': {'script_type': 'arabic', 'reading_direction': 'rtl', 'font_family': 'Noto Sans Arabic'},
            'ar': {'script_type': 'arabic', 'reading_direction': 'rtl', 'font_family': 'Noto Sans Arabic'},
            'bn': {'script_type': 'bengali', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Bengali'},
            'ta': {'script_type': 'tamil', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Tamil'},
            'ml': {'script_type': 'malayalam', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Malayalam'},
            'kn': {'script_type': 'kannada', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Kannada'},
            'gu': {'script_type': 'gujarati', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Gujarati'},
            'pa': {'script_type': 'gurmukhi', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Gurmukhi'},
            'or': {'script_type': 'odia', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Odia'},
            'as': {'script_type': 'bengali', 'reading_direction': 'ltr', 'font_family': 'Noto Sans Bengali'},
        }
        
        return script_mapping.get(language, {
            'script_type': 'latin', 
            'reading_direction': 'ltr', 
            'font_family': 'Noto Sans'
        })
    
    @classmethod
    def is_supported_language(cls, language: str) -> bool:
        """Check if language is supported for question generation"""
        supported_languages = [
            'en', 'hi', 'te', 'ur', 'ar', 'bn', 'ta', 'ml', 'kn', 'gu', 'mr', 'pa', 'or', 'as',
            'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh', 'ja', 'ko', 'th', 'vi', 'id', 'ms'
        ]
        return language in supported_languages