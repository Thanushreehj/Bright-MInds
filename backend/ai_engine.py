# backend/ai_engine.py - AI Model Wrapper

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os
from pathlib import Path

class AIModelManager:
    """Singleton manager for AI model to avoid reloading"""
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_model(self, model_name='all-MiniLM-L6-v2'):
        if self._model is None:
            print(f"🔄 Loading AI model: {model_name}...")
            # Use models directory for cache
            cache_dir = Path(__file__).parent / 'models'
            cache_dir.mkdir(exist_ok=True)
            
            self._model = SentenceTransformer(model_name, cache_folder=str(cache_dir))
            print("✅ AI model loaded successfully!")
        return self._model

class IntentClassifier:
    """Intent classification using semantic similarity"""
    
    def __init__(self, intents_data=None):
        self.model_manager = AIModelManager()
        self.model = self.model_manager.get_model()
        self.intents = []
        self.intent_embeddings = None
        self.intent_mapping = {}
        self._init_default_intents()
        
        if intents_data:
            self.load_intents(intents_data)
    
    def _init_default_intents(self):
        """Initialize default intents"""
        self.intents = [
            "hello", "hi", "hey", "good morning",
            "bye", "goodbye", "see you",
            "thank you", "thanks",
            "tell me about courses", "what subjects", "learning",
            "math help", "addition", "subtraction", "multiplication",
            "english help", "grammar", "vocabulary",
            "adhd", "autism", "dyslexia", "learning disability",
            "games", "play", "activities",
            "quiz", "assessment", "test",
            "learning tip", "study better",
            "fun fact", "interesting fact"
        ]
        
        self.intent_mapping = {
            "hello": "greet", "hi": "greet", "hey": "greet", "good morning": "greet",
            "bye": "farewell", "goodbye": "farewell", "see you": "farewell",
            "thank you": "thanks", "thanks": "thanks",
            "tell me about courses": "courses", "what subjects": "courses", "learning": "courses",
            "math help": "math", "addition": "math", "subtraction": "math", "multiplication": "math",
            "english help": "english", "grammar": "english", "vocabulary": "english",
            "adhd": "adhd", "autism": "autism", "dyslexia": "dyslexia", "learning disability": "dyslexia",
            "games": "games", "play": "games", "activities": "games",
            "quiz": "quiz", "assessment": "quiz", "test": "quiz",
            "learning tip": "tip", "study better": "tip",
            "fun fact": "fact", "interesting fact": "fact"
        }
        
        self._create_embeddings()
    
    def load_intents(self, intents_file):
        """Load intents from JSON file"""
        if os.path.exists(intents_file):
            with open(intents_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'intents' in data:
                self.intents = list(data['intents'].keys())
                self._create_embeddings()
    
    def _create_embeddings(self):
        """Create embeddings for all intents"""
        if self.intents:
            self.intent_embeddings = self.model.encode(self.intents)
    
    def classify(self, text, threshold=0.3):
        """Classify text to best matching intent"""
        if not self.intents or self.intent_embeddings is None:
            return 'default', 0.0
        
        text_embedding = self.model.encode([text])
        similarities = cosine_similarity(text_embedding, self.intent_embeddings)[0]
        
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score > threshold:
            matched_intent = self.intents[best_idx]
            category = self.intent_mapping.get(matched_intent, 'default')
            return category, float(best_score)
        
        return 'default', float(best_score)

class ResponseGenerator:
    """Generate responses based on intent"""
    
    def __init__(self, responses_file=None):
        self.responses = {}
        self.fallbacks = []
        self._init_default_responses()
        
        if responses_file:
            self.load_responses(responses_file)
    
    def _init_default_responses(self):
        """Initialize default responses"""
        self.responses = {
            'greet': [
                "👋 Hello! I'm Minnie, your AI learning companion!",
                "🌟 Hi there! Ready for some fun learning?",
                "😊 Welcome! How can I help you today?"
            ],
            'farewell': [
                "👋 Goodbye! Keep learning!",
                "🌟 See you later!",
                "💛 Take care!"
            ],
            'thanks': [
                "You're welcome! 😊",
                "🌟 My pleasure!",
                "💛 Anytime!"
            ],
            'courses': [
                "📚 We offer Math, English, and General Knowledge courses!"
            ],
            'math': [
                "➕ Math topics: Numbers, Addition, Subtraction, Multiplication!"
            ],
            'english': [
                "📖 English topics: Grammar, Vocabulary, Reading, Writing!"
            ],
            'adhd': [
                "💡 ADHD affects focus. Try our short, engaging activities!"
            ],
            'autism': [
                "💙 We have calm, structured activities for autistic learners!"
            ],
            'dyslexia': [
                "📝 Try our multi-sensory word games for dyslexia support!"
            ],
            'games': [
                "🎮 Play Memory Match, Word Scramble, and Pattern Play!"
            ],
            'quiz': [
                "📝 Take our adaptive assessment to test your knowledge!"
            ],
            'tip': [
                "💡 Try the Pomodoro technique: 15 min study, 5 min break!"
            ],
            'fact': [
                "🌟 Did you know? Octopuses have three hearts!"
            ],
            'about': [
                "🌟 Bright Minds helps every child learn at their own pace!"
            ],
            'default': [
                "🤔 I'm not sure. Can you rephrase?",
                "😊 I can help with courses, games, or learning tips!"
            ]
        }
    
    def load_responses(self, responses_file):
        """Load response templates from JSON"""
        if os.path.exists(responses_file):
            with open(responses_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if 'intents' in loaded:
                    for intent, data in loaded['intents'].items():
                        if 'responses' in data:
                            self.responses[intent] = data['responses']
    
    def get_response(self, intent):
        """Get a random response for the intent"""
        import random
        responses = self.responses.get(intent, self.responses.get('default', ["I'm not sure about that."]))
        return random.choice(responses)

class ConversationMemory:
    """Store and manage conversation history"""
    
    def __init__(self, max_history=20):
        self.memory = {}
        self.max_history = max_history
    
    def add_message(self, session_id, user_message, bot_response, intent):
        """Add a message to conversation history"""
        if session_id not in self.memory:
            self.memory[session_id] = []
        
        self.memory[session_id].append({
            'user': user_message,
            'bot': bot_response,
            'intent': intent
        })
        
        # Trim history
        if len(self.memory[session_id]) > self.max_history:
            self.memory[session_id] = self.memory[session_id][-self.max_history:]
    
    def get_history(self, session_id):
        """Get conversation history for a session"""
        return self.memory.get(session_id, [])
    
    def clear_session(self, session_id):
        """Clear conversation history for a session"""
        if session_id in self.memory:
            del self.memory[session_id]
    
    def get_context(self, session_id, last_n=3):
        """Get last N messages for context"""
        history = self.get_history(session_id)
        return history[-last_n:] if history else []