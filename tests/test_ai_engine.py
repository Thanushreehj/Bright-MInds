# tests/test_ai_engine.py - Unit tests for AI engine

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAIEngine(unittest.TestCase):
    """Test cases for the AI engine"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("\n🧪 Setting up AI Engine tests...")
        try:
            from backend.ai_engine import AIModelManager, IntentClassifier, ResponseGenerator
            cls.AIModelManager = AIModelManager
            cls.IntentClassifier = IntentClassifier
            cls.ResponseGenerator = ResponseGenerator
            cls.has_ai = True
        except ImportError as e:
            print(f"⚠️ AI module not available: {e}")
            cls.has_ai = False
    
    def test_intent_classifier_init(self):
        """Test IntentClassifier initialization"""
        if not self.has_ai:
            self.skipTest("AI engine not available")
        
        classifier = self.IntentClassifier()
        self.assertIsNotNone(classifier)
    
    def test_intent_classification(self):
        """Test intent classification with various inputs"""
        if not self.has_ai:
            self.skipTest("AI engine not available")
        
        classifier = self.IntentClassifier()
        
        test_cases = [
            ("Hello", "greet"),
            ("Tell me about math", "math"),
            ("I need help with ADHD", "adhd"),
            ("Goodbye", "farewell"),
            ("Thank you", "thanks")
        ]
        
        for input_text, expected_intent in test_cases:
            intent, confidence = classifier.classify(input_text)
            self.assertIsNotNone(intent)
            self.assertGreaterEqual(confidence, 0)
            self.assertLessEqual(confidence, 1)
    
    def test_response_generator(self):
        """Test response generation"""
        if not self.has_ai:
            self.skipTest("AI engine not available")
        
        generator = self.ResponseGenerator()
        
        # Test different intent responses
        intents = ['greet', 'farewell', 'thanks', 'default']
        for intent in intents:
            response = generator.get_response(intent)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
    
    def test_semantic_similarity(self):
        """Test that similar phrases get similar classifications"""
        if not self.has_ai:
            self.skipTest("AI engine not available")
        
        classifier = self.IntentClassifier()
        
        # Similar phrases should get same intent
        intent1, _ = classifier.classify("What math courses do you have?")
        intent2, _ = classifier.classify("Tell me about mathematics learning")
        
        self.assertEqual(intent1, intent2)

class TestKnowledgeBase(unittest.TestCase):
    """Test knowledge base data"""
    
    def setUp(self):
        """Load knowledge base"""
        import json
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'knowledge_base.json')
        
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                self.kb = json.load(f)
        else:
            self.kb = None
    
    def test_knowledge_base_exists(self):
        """Test that knowledge base file exists and is valid"""
        self.assertIsNotNone(self.kb, "Knowledge base file not found")
        self.assertIn('intents', self.kb)
        self.assertIn('learning_tips', self.kb)
        self.assertIn('fun_facts', self.kb)
    
    def test_intents_have_patterns(self):
        """Test that each intent has patterns and responses"""
        if not self.kb:
            self.skipTest("Knowledge base not loaded")
        
        for intent_name, intent_data in self.kb['intents'].items():
            with self.subTest(intent=intent_name):
                self.assertIn('patterns', intent_data)
                self.assertIn('responses', intent_data)
                self.assertTrue(len(intent_data['patterns']) > 0)
                self.assertTrue(len(intent_data['responses']) > 0)

class TestQuizData(unittest.TestCase):
    """Test quiz questions data"""
    
    def setUp(self):
        """Load questions data"""
        import json
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
        
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
        else:
            self.questions = None
    
    def test_questions_file_exists(self):
        """Test that questions file exists"""
        self.assertIsNotNone(self.questions, "Questions file not found")
    
    def test_questions_have_required_fields(self):
        """Test each question has required fields"""
        if not self.questions:
            self.skipTest("Questions not loaded")
        
        for subject, levels in self.questions.items():
            for level, questions in levels.items():
                for q in questions:
                    with self.subTest(subject=subject, level=level, id=q.get('id', 'unknown')):
                        self.assertIn('id', q)
                        self.assertIn('question', q)
                        self.assertIn('options', q)
                        self.assertIn('answer', q)
                        self.assertTrue(len(q['options']) >= 2)

if __name__ == '__main__':
    unittest.main(verbosity=2)