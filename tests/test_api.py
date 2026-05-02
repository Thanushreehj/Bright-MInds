# tests/test_api.py - API endpoint tests

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAPI(unittest.TestCase):
    """Test cases for API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test Flask app"""
        print("\n🧪 Setting up API tests...")
        try:
            from backend.app import app
            cls.app = app
            cls.client = app.test_client()
            cls.app_ready = True
        except Exception as e:
            print(f"⚠️ Could not initialize Flask app: {e}")
            cls.app_ready = False
    
    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'online')
    
    def test_chat_endpoint(self):
        """Test /api/chat endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        test_messages = [
            "Hello",
            "Tell me about math",
            "What is ADHD?",
            "Goodbye"
        ]
        
        for message in test_messages:
            with self.subTest(message=message):
                response = self.client.post('/api/chat',
                    json={'message': message, 'session_id': 'test_session'},
                    content_type='application/json'
                )
                self.assertEqual(response.status_code, 200)
                
                data = json.loads(response.data)
                self.assertIn('response', data)
                self.assertIsInstance(data['response'], str)
                self.assertTrue(len(data['response']) > 0)
    
    def test_chat_endpoint_with_mood(self):
        """Test chat endpoint with mood parameter"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.post('/api/chat',
            json={
                'message': "I'm feeling happy today",
                'session_id': 'test_session',
                'mood': 'happy'
            },
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
    
    def test_chat_endpoint_empty_message(self):
        """Test chat endpoint with empty message"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.post('/api/chat',
            json={'message': '', 'session_id': 'test_session'},
            content_type='application/json'
        )
        
        # Should return 400 for empty message
        self.assertEqual(response.status_code, 400)
    
    def test_learning_style_endpoint(self):
        """Test /api/assess-learning-style endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        test_answers = {
            'q1': "I like to see pictures and diagrams",
            'q2': "I prefer watching videos",
            'q3': "I learn by doing hands-on activities"
        }
        
        response = self.client.post('/api/assess-learning-style',
            json={'answers': test_answers},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('learning_style', data)
        self.assertIn('recommendation', data)
    
    def test_get_tip_endpoint(self):
        """Test /api/get-tip endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.get('/api/get-tip')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tip', data)
        self.assertIsInstance(data['tip'], str)
    
    def test_get_fact_endpoint(self):
        """Test /api/get-fact endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.get('/api/get-fact')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('fact', data)
        self.assertIsInstance(data['fact'], str)
    
    def test_session_clear_endpoint(self):
        """Test session clear endpoint"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        # First send a message to create session
        self.client.post('/api/chat',
            json={'message': 'Hello', 'session_id': 'clear_test'},
            content_type='application/json'
        )
        
        # Then clear the session
        response = self.client.delete('/api/session/clear_test')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertTrue(data['success'])

class TestAPIResponseStructure(unittest.TestCase):
    """Test API response structure"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client"""
        try:
            from backend.app import app
            cls.client = app.test_client()
            cls.app_ready = True
        except:
            cls.app_ready = False
    
    def test_chat_response_structure(self):
        """Test chat response has correct structure"""
        if not self.app_ready:
            self.skipTest("Flask app not available")
        
        response = self.client.post('/api/chat',
            json={'message': 'Hello', 'session_id': 'test'},
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        # Check required fields
        required_fields = ['response', 'suggestions', 'intent', 'confidence']
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, data)
        
        # Check data types
        self.assertIsInstance(data['response'], str)
        self.assertIsInstance(data['suggestions'], list)
        self.assertIsInstance(data['intent'], str)
        self.assertIsInstance(data['confidence'], (int, float))

if __name__ == '__main__':
    # Run tests with more verbose output
    unittest.main(verbosity=2)