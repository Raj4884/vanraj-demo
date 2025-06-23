import requests
from bs4 import BeautifulSoup
import os
import json
import re

class HealthAnalyzer:
    def __init__(self):
        self.cache_dir = 'data/health_cache'
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def analyze_symptoms(self, symptoms):
        """
        Analyze symptoms and provide possible diagnoses and recommendations
        
        This is a simplified version that searches for health information online.
        In a production environment, you would use a medical API with proper licensing.
        """
        # Clean and prepare symptoms
        symptoms_query = self._prepare_query(symptoms)
        
        # Check cache first
        cache_result = self._check_cache(symptoms_query)
        if cache_result:
            return cache_result
        
        # Perform web search for health information
        search_results = self._search_health_info(symptoms_query)
        
        # Process and analyze results
        analysis = self._process_results(search_results, symptoms)
        
        # Cache the results
        self._cache_results(symptoms_query, analysis)
        
        return analysis
    
    def _prepare_query(self, symptoms):
        """Prepare search query from symptoms"""
        # Remove special characters and normalize
        clean_symptoms = re.sub(r'[^\w\s]', '', symptoms.lower())
        return clean_symptoms.strip()
    
    def _check_cache(self, query):
        """Check if we have cached results for this query"""
        cache_file = os.path.join(self.cache_dir, f"{query.replace(' ', '_')}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        return None
    
    def _search_health_info(self, query):
        """
        Search for health information online
        
        Note: In a production environment, you would use a medical API with proper licensing.
        This is a simplified version for demonstration purposes.
        """
        try:
            # This is a placeholder. In a real application, you would use a medical API
            # or a more sophisticated web scraping approach with proper permissions.
            search_url = f"https://www.google.com/search?q=health+information+{query.replace(' ', '+')}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            print(f"Error searching health information: {e}")
            return None
    
    def _process_results(self, html_content, original_symptoms):
        """Process and analyze search results"""
        if not html_content:
            return self._get_fallback_response(original_symptoms)
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract relevant information (this is simplified)
            # In a real application, you would use more sophisticated NLP techniques
            
            # Placeholder for demonstration
            possible_conditions = [
                "Common cold",
                "Seasonal allergies",
                "Stress-related symptoms"
            ]
            
            recommendations = [
                "Rest and stay hydrated",
                "Consider over-the-counter medications appropriate for your symptoms",
                "If symptoms persist for more than a few days, consult a healthcare professional"
            ]
            
            disclaimer = (
                "IMPORTANT: This is not a medical diagnosis. The information provided is for "
                "educational purposes only and should not replace professional medical advice. "
                "Always consult with a qualified healthcare provider for proper diagnosis and treatment."
            )
            
            return {
                "symptoms": original_symptoms,
                "possible_conditions": possible_conditions,
                "recommendations": recommendations,
                "disclaimer": disclaimer,
                "seek_medical_attention": self._should_seek_medical_attention(original_symptoms)
            }
        except Exception as e:
            print(f"Error processing health information: {e}")
            return self._get_fallback_response(original_symptoms)
    
    def _should_seek_medical_attention(self, symptoms):
        """
        Check if symptoms suggest immediate medical attention is needed
        
        This is a very simplified version. In a real application, you would use
        a more sophisticated algorithm based on medical guidelines.
        """
        urgent_keywords = [
            "chest pain", "difficulty breathing", "shortness of breath", 
            "severe pain", "unconscious", "unresponsive", "stroke", 
            "heart attack", "bleeding", "head injury", "seizure"
        ]
        
        symptoms_lower = symptoms.lower()
        for keyword in urgent_keywords:
            if keyword in symptoms_lower:
                return True
        
        return False
    
    def _get_fallback_response(self, symptoms):
        """Provide a fallback response when analysis fails"""
        return {
            "symptoms": symptoms,
            "possible_conditions": ["Unable to analyze symptoms"],
            "recommendations": [
                "If you're experiencing concerning symptoms, please consult with a healthcare professional",
                "For general health questions, consider reliable sources like CDC.gov or WHO.int"
            ],
            "disclaimer": (
                "IMPORTANT: This is not a medical diagnosis. The information provided is for "
                "educational purposes only and should not replace professional medical advice. "
                "Always consult with a qualified healthcare provider for proper diagnosis and treatment."
            ),
            "seek_medical_attention": False
        }
    
    def _cache_results(self, query, results):
        """Cache the analysis results"""
        cache_file = os.path.join(self.cache_dir, f"{query.replace(' ', '_')}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"Error caching results: {e}")