# backend/app.py - Enhanced with better conversation handling and feature links

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import random
import re
from datetime import datetime
from difflib import SequenceMatcher

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ============================================================
# ENHANCED AI ENGINE WITH BETTER CONVERSATION HANDLING
# ============================================================

class EnhancedAI:
    """Enhanced AI with better conversation flow and feature links"""
    
    def __init__(self):
        self.load_knowledge_base()
        self.conversation_context = {}  # Track conversation context per session
        self.last_intent = {}  # Track last intent for follow-ups
    
    def load_knowledge_base(self):
        """Load knowledge base with enhanced responses"""
        
        # Intent patterns with keywords
        self.intents = {
            'greet': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'namaste', 'howdy'],
            'farewell': ['bye', 'goodbye', 'see you', 'later', 'take care', 'good night'],
            'thanks': ['thank', 'thanks', 'thx', 'ty', 'appreciate'],
            'courses': ['course', 'subjects', 'what can i learn', 'study', 'learn', 'recommend'],
            'math': ['math', 'maths', 'numbers', 'addition', 'subtraction', 'multiplication', 'division', 'count'],
            'english': ['english', 'grammar', 'vocabulary', 'spelling', 'reading', 'writing', 'words'],
            'gk': ['gk', 'general knowledge', 'science', 'geography', 'history', 'facts', 'world'],
            'adhd': ['adhd', 'attention', 'focus', 'hyperactive', 'impulsive', 'concentrate'],
            'autism': ['autism', 'autistic', 'asd', 'spectrum', 'social', 'sensory'],
            'dyslexia': ['dyslexia', 'reading difficulty', 'spelling', 'letter reversal', 'learning disability'],
            'games': ['game', 'games', 'play', 'fun', 'activity', 'memory', 'puzzle'],
            'quiz': ['quiz', 'test', 'assessment', 'exam', 'practice', 'challenge', 'take test'],
            'tip': ['tip', 'advice', 'strategy', 'how to study', 'remember', 'technique'],
            'fact': ['fact', 'did you know', 'interesting', 'surprise me', 'tell me something'],
            'help': ['help', 'what can you do', 'support', 'guide', 'tutorial', 'features'],
            'about_platform': ['about bright minds', 'what is this', 'platform', 'website', 'features list'],
            'progress': ['progress', 'track', 'score', 'my results', 'how am i doing'],
            'recommendation': ['recommend', 'suggest', 'what should i do', 'where to start']
        }
        
        # Enhanced responses with HTML links
        self.responses = {
            'greet': [
                "👋 Hello! I'm Minnie, your AI learning companion! What would you like to learn today?",
                "🌟 Hi there! Ready for some fun learning? I can help with Math, English, and more!",
                "😊 Welcome back! How can I help you learn something new today?"
            ],
            'farewell': [
                "👋 Goodbye! Keep shining bright! Come back anytime!",
                "🌟 See you later! Remember, every day is a learning day!",
                "💛 Take care! I'll be here when you need me!"
            ],
            'thanks': [
                "You're welcome! 😊 Always happy to help!",
                "🌟 My pleasure! Keep up the great learning!",
                "💛 Anytime! That's what I'm here for!"
            ],
            'courses': [
                "📚 **Bright Minds Courses:**\n\n🔢 **Mathematics** - Numbers, addition, subtraction, multiplication, word problems\n📖 **English** - Grammar, vocabulary, reading comprehension\n🌍 **General Knowledge** - Science, geography, animals, fun facts\n\n👉 <a href='/courses.html' style='color:#6C63FF; font-weight:bold;'>View All Courses →</a>\n\nWhich subject interests you most?"
            ],
            'math': [
                "➕ **Mathematics Course** includes:\n\n• Counting and number recognition\n• Addition & subtraction with visuals\n• Multiplication tables (2-12)\n• Word problems with real-life scenarios\n• Fractions and basic geometry\n\n🎯 <a href='/assessment.html' style='color:#6C63FF; font-weight:bold;'>Take Math Quiz →</a>\n\n📚 <a href='/courses.html' style='color:#6C63FF; font-weight:bold;'>Explore Math Course →</a>"
            ],
            'english': [
                "📖 **English Course** includes:\n\n• Alphabet & phonics (beginner)\n• Sight words and vocabulary building\n• Grammar: nouns, verbs, adjectives\n• Sentence construction\n• Reading comprehension with stories\n\n🎯 <a href='/assessment.html' style='color:#6C63FF; font-weight:bold;'>Take English Quiz →</a>\n\n📚 <a href='/courses.html' style='color:#6C63FF; font-weight:bold;'>Explore English Course →</a>"
            ],
            'gk': [
                "🌍 **General Knowledge Course** includes:\n\n• Animals and their habitats 🦁\n• Solar system and space 🌟\n• Countries and capitals 🗺️\n• Science facts 🔬\n• Famous inventors and discoveries 💡\n\n🎯 <a href='/assessment.html' style='color:#6C63FF; font-weight:bold;'>Take GK Quiz →</a>\n\n📚 <a href='/courses.html' style='color:#6C63FF; font-weight:bold;'>Explore GK Course →</a>"
            ],
            'adhd': [
                "💡 **ADHD (Attention Deficit Hyperactivity Disorder)** affects focus, impulse control, and activity levels.\n\n**How Bright Minds helps:**\n✓ Short, engaging activities (10-15 min)\n✓ Immediate feedback and rewards\n✓ Minimized distractions\n✓ Break tasks into small steps\n\n🎮 <a href='/games.html' style='color:#6C63FF; font-weight:bold;'>Try ADHD-Friendly Games →</a>\n\n📚 <a href='/disability.html' style='color:#6C63FF; font-weight:bold;'>Learn More About ADHD →</a>"
            ],
            'autism': [
                "💙 **Autism Spectrum Disorder (ASD)** affects communication and sensory processing.\n\n**Bright Minds features:**\n✓ Predictable, structured lessons\n✓ Visual learning emphasis\n✓ Calm, low-stimulation design\n✓ Option to repeat and review\n\n🎮 <a href='/games.html' style='color:#6C63FF; font-weight:bold;'>Try Calming Games →</a>\n\n📚 <a href='/disability.html' style='color:#6C63FF; font-weight:bold;'>Learn More About Autism →</a>"
            ],
            'dyslexia': [
                "📝 **Dyslexia** affects reading, spelling, and writing — but NOT intelligence!\n\n**How we help:**\n✓ Multi-sensory learning\n✓ Readable fonts and colors\n✓ Audio support\n✓ Word games\n\n🎮 <a href='/games.html' style='color:#6C63FF; font-weight:bold;'>Try Word Games →</a>\n\n📚 <a href='/disability.html' style='color:#6C63FF; font-weight:bold;'>Learn More About Dyslexia →</a>"
            ],
            'games': [
                "🎮 **Available Games:**\n\n🃏 **Memory Match** - Build focus and memory\n🔤 **Word Scramble** - Improve spelling\n🔢 **Pattern Play** - Develop thinking skills\n\n👉 <a href='/games.html' style='color:#6C63FF; font-weight:bold;'>Play Games Now →</a>\n\nWhich game would you like to try?"
            ],
            'quiz': [
                "📝 **Ready to test your knowledge?**\n\nOur AI-powered assessment features:\n✓ 10 adaptive questions\n✓ Difficulty adjusts to YOUR level\n✓ Instant scoring\n✓ Personalized feedback\n✓ Course recommendations\n\n👉 <a href='/assessment.html' style='color:#6C63FF; font-weight:bold; background:#F3F0FF; padding:8px 16px; border-radius:25px;'>Take AI Assessment Now →</a>\n\nThis will help me understand your learning level better!"
            ],
            'tip': None,  # Dynamic
            'fact': None,  # Dynamic
            'help': [
                "🆘 **Here's what I can help you with:**\n\n📚 **Courses** - Math, English, GK\n   <a href='/courses.html' style='color:#6C63FF;'>Browse Courses →</a>\n\n🎮 **Games** - Memory, Word, Pattern games\n   <a href='/games.html' style='color:#6C63FF;'>Play Games →</a>\n\n📝 **Assessments** - Adaptive quizzes\n   <a href='/assessment.html' style='color:#6C63FF;'>Take a Test →</a>\n\n🧠 **Learning Differences** - ADHD, Autism, Dyslexia\n   <a href='/disability.html' style='color:#6C63FF;'>Learn More →</a>\n\n💡 **Tips & Facts** - Learning strategies\n\nWhat would you like to explore?"
            ],
            'about_platform': [
                "🌟 **About Bright Minds**\n\n**Mission:** Make learning accessible, fun, and adaptive for every child, especially those with different learning needs.\n\n**Features:**\n✓ AI-Powered Tutor (that's me!)\n✓ Adaptive Assessments\n✓ Educational Games\n✓ Disability Awareness Resources\n✓ Personalized Learning Paths\n\n**Team:** Passionate educators and developers\n\n👉 <a href='/about.html' style='color:#6C63FF; font-weight:bold;'>Meet the Team →</a>"
            ],
            'progress': [
                "📊 **Track Your Progress**\n\nTo see your learning progress:\n1. Take the <a href='/assessment.html' style='color:#6C63FF;'>AI Assessment</a>\n2. Complete courses in <a href='/courses.html' style='color:#6C63FF;'>Courses</a>\n3. Play <a href='/games.html' style='color:#6C63FF;'>Learning Games</a>\n\nYour scores help me recommend the best next steps! 🎯\n\nReady to start your learning journey?"
            ],
            'recommendation': [
                "🎯 **Personalized Recommendation**\n\nBased on common learning paths, I suggest:\n\n1️⃣ Start with the <a href='/assessment.html' style='color:#6C63FF; font-weight:bold;'>AI Assessment</a> - It helps me understand your level\n\n2️⃣ Explore <a href='/courses.html' style='color:#6C63FF;'>Beginner Courses</a> - Math or English are great starts\n\n3️⃣ Try <a href='/games.html' style='color:#6C63FF;'>Learning Games</a> - Fun way to build skills\n\nWhat would you like to do first?"
            ],
            'default': [
                "🤔 I'm not sure about that. Let me help you better!\n\n**Here's what I can do:**\n• 📚 <a href='/courses.html' style='color:#6C63FF;'>Show Courses</a>\n• 🎮 <a href='/games.html' style='color:#6C63FF;'>Play Games</a>\n• 📝 <a href='/assessment.html' style='color:#6C63FF;'>Take a Test</a>\n• 💡 Give Learning Tips\n• 🧠 Explain ADHD/Autism\n\nWhat would you like to explore?"
            ]
        }
        
        # Dynamic content
        self.learning_tips = [
            "🎯 **Pomodoro Technique:** Study 15 minutes, then take a 5-minute break. This helps maintain focus!",
            "🎵 **Music helps memory:** Try singing spelling words or math facts to a catchy tune!",
            "🎨 **Color coding:** Use different colors for different subjects. It helps organize information!",
            "🧘 **Deep breaths before studying:** 3 deep breaths can calm your mind and improve focus!",
            "⭐ **Celebrate small wins:** Finished a chapter? Got answers right? Celebrate! You're making progress!",
            "🔄 **Review what you learned:** Spend 5 minutes reviewing yesterday's lesson. It locks information into memory!",
            "🎮 **Turn practice into a game:** Set a timer and challenge yourself to beat your own score!",
            "📖 **Read aloud:** Reading out loud helps with comprehension and focus, especially for struggling readers.",
            "💤 **Sleep matters:** Getting enough sleep helps your brain store everything you learned!",
            "📝 **Write it down:** Taking notes by hand helps you remember better than typing!",
            "👥 **Study with others:** Explaining concepts to someone else helps you understand better!",
            "🏆 **Set small goals:** Break big tasks into smaller, achievable goals. Each one is a victory!"
        ]
        
        self.fun_facts = [
            "🐙 Octopuses have THREE hearts! Two pump blood to the gills, and one pumps it to the rest of the body!",
            "🍯 Honey never expires. Archaeologists found 3000-year-old honey in Egyptian tombs that was still good!",
            "🐘 Elephants are the only mammals that can't jump. But they have the best memory in the animal kingdom!",
            "🌍 Earth is the only planet in our solar system not named after a Roman or Greek god.",
            "🦋 A group of flamingos is called a 'flamboyance' — so fitting!",
            "📚 The word 'school' comes from the Greek 'skholē' which originally meant 'leisure' or 'free time'!",
            "🌱 A single tree can absorb up to 48 pounds of carbon dioxide per year!",
            "🐧 Penguins propose to their mates with a pebble — the best pebble wins the heart!",
            "🦒 A giraffe's tongue is 21 inches long — that's longer than a ruler!",
            "🐋 Blue whales are louder than jet engines — their calls can be heard 1,000 miles away!"
        ]
        
        # Mood responses
        self.mood_responses = {
            'happy': "😊 That's wonderful! A happy mind learns best. Let's make today's learning session extra fun! What would you like to explore? 🎉",
            'excited': "🤩 I love your energy! Let's channel that excitement into something amazing — maybe a <a href='/assessment.html' style='color:#6C63FF;'>quiz</a> or a <a href='/games.html' style='color:#6C63FF;'>game</a>?",
            'calm': "😌 A calm mind is ready to learn. This is the perfect state for focused study. What shall we explore today? 📚",
            'tired': "😴 Feeling tired? That's okay! Let's start with something light — maybe a <a href='/games.html' style='color:#6C63FF;'>fun game</a> or a <a href='#' onclick='sendQuick(\"Tell me a fun fact\")'>fun fact</a>?",
            'confused': "😕 No worries — confusion is the first step to learning! Tell me what's puzzling you, or try our <a href='/assessment.html' style='color:#6C63FF;'>assessment</a> to find your level!",
            'sad': "💛 I'm sorry you're feeling down. You're brave for showing up anyway. Let's do something gentle — a <a href='/games.html' style='color:#6C63FF;'>calming game</a> or a <a href='#' onclick='sendQuick(\"Tell me a fun fact\")'>fun fact</a>?"
        }
    
    def get_similarity(self, a, b):
        """Calculate string similarity"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def match_intent(self, text, session_id=None):
        """Match user input to closest intent with context awareness"""
        text_lower = text.lower()
        
        # Check for mood first
        mood = self.detect_mood(text_lower)
        if mood:
            return 'mood', 1.0, mood
        
        # Check for follow-up questions based on last intent
        if session_id and session_id in self.last_intent:
            last = self.last_intent[session_id]
            # Handle follow-ups like "tell me more", "continue", "and?"
            if any(word in text_lower for word in ['more', 'continue', 'tell me more', 'and', 'also', 'what else']):
                if last in self.responses:
                    return last, 0.8, None
        
        # Score each intent
        scores = {}
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 2  # Exact match
                # Check for partial matches
                elif len(keyword) > 3 and keyword in text_lower:
                    score += 1
            scores[intent] = score
        
        # Get best match
        if scores:
            best_intent = max(scores, key=scores.get)
            best_score = scores[best_intent]
            if best_score > 0:
                return best_intent, best_score, None
        
        return 'help', 0, None
    
    def detect_mood(self, text):
        """Detect mood from text"""
        mood_map = {
            'happy': ['happy', 'great', 'wonderful', 'good', 'fantastic', 'awesome', 'amazing', 'excellent'],
            'excited': ['excited', 'thrilled', 'pumped', 'energized', 'enthusiastic'],
            'calm': ['calm', 'relaxed', 'peaceful', 'chill', 'zen'],
            'tired': ['tired', 'sleepy', 'exhausted', 'drained', 'fatigued', 'worn out'],
            'confused': ['confused', 'confusing', 'puzzled', 'lost', 'unclear', 'don\'t understand'],
            'sad': ['sad', 'down', 'unhappy', 'depressed', 'gloomy', 'upset']
        }
        
        for mood, keywords in mood_map.items():
            for keyword in keywords:
                if keyword in text:
                    return mood
        return None
    
    def get_response(self, intent, mood=None, session_id=None):
        """Get response based on intent with context"""
        import random
        
        # Store last intent for context
        if session_id:
            self.last_intent[session_id] = intent
        
        if intent == 'mood' and mood:
            return self.mood_responses.get(mood, "😊 Thanks for sharing how you feel!")
        
        if intent == 'tip':
            tip = random.choice(self.learning_tips)
            return f"💡 **Learning Tip #{random.randint(1, 100)}:**\n\n{tip}\n\n✨ Would you like another tip? Just ask 'another tip'!"
        
        if intent == 'fact':
            fact = random.choice(self.fun_facts)
            return f"🌟 **Did you know?**\n\n{fact}\n\n🎉 Want another fun fact? Just say 'another fact'!"
        
        responses = self.responses.get(intent, self.responses['default'])
        return random.choice(responses)
    
    def get_suggestions(self, intent):
        """Get follow-up suggestions based on intent"""
        suggestions_map = {
            'greet': ['Tell me about courses', 'What games can I play?', 'Give me a tip', 'Tell me a fact'],
            'courses': ['Tell me about Math', 'Tell me about English', 'Take a quiz', 'Tell me about GK'],
            'math': ['Practice math', 'Take math quiz', 'Tell me about English', 'Show me math games'],
            'english': ['Practice spelling', 'Take English quiz', 'Tell me about GK', 'Grammar help'],
            'gk': ['Tell me a fun fact', 'Take GK quiz', 'Tell me about science', 'Animal facts'],
            'adhd': ['ADHD learning tips', 'ADHD-friendly games', 'Talk about Autism', 'Focus strategies'],
            'autism': ['Autism learning tips', 'Calming activities', 'Talk about ADHD', 'Visual learning'],
            'dyslexia': ['Word games', 'Reading strategies', 'Talk about ADHD', 'Spelling help'],
            'games': ['Play Memory match', 'Try Word scramble', 'Play Pattern game', 'Tell me about courses'],
            'quiz': ['Take assessment now', 'Practice questions', 'Tell me about courses', 'Math quiz'],
            'tip': ['Another tip please', 'Tell me a fun fact', 'Show me courses', 'Take a quiz'],
            'fact': ['Another fun fact', 'Tell me a learning tip', 'Show me games', 'GK quiz'],
            'help': ['What courses are available?', 'Tell me about ADHD', 'Show me games', 'Give me a tip'],
            'about_platform': ['Tell me about courses', 'Show me features', 'Meet the team'],
            'progress': ['Take an assessment', 'View courses', 'Play games'],
            'recommendation': ['Take assessment', 'View courses', 'Try games'],
            'default': ['Show me courses', 'Give me a learning tip', 'Tell me a fun fact', 'What games can I play?']
        }
        
        suggestions = suggestions_map.get(intent, suggestions_map['default'])
        random.shuffle(suggestions)
        return suggestions[:4]

# Initialize AI engine
print("🤖 Initializing Enhanced AI Engine...")
ai_engine = EnhancedAI()
print("✅ AI Engine Ready!")

# Store conversation history with timestamps
conversation_history = {}

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def serve_index():
    """Serve the main page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend files"""
    return send_from_directory('../frontend', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint with enhanced features"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        mood = data.get('mood', None)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Match intent with context
        intent, confidence, detected_mood = ai_engine.match_intent(user_message, session_id)
        
        # Use detected mood if not explicitly provided
        if detected_mood and not mood:
            mood = detected_mood
        
        # Get response
        response = ai_engine.get_response(intent, mood, session_id)
        suggestions = ai_engine.get_suggestions(intent)
        
        # Store in conversation history
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        conversation_history[session_id].append({
            'user': user_message,
            'bot': response,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 30 messages (increased for longer conversations)
        if len(conversation_history[session_id]) > 30:
            conversation_history[session_id] = conversation_history[session_id][-30:]
        
        return jsonify({
            'success': True,
            'response': response,
            'suggestions': suggestions,
            'intent': intent,
            'confidence': float(confidence)
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'response': "I'm having a little trouble. Please try again! 🤔",
            'suggestions': ['Tell me about courses', 'Give me a tip', 'Tell me a fact']
        }), 500

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history for a session"""
    if session_id in conversation_history:
        return jsonify({
            'success': True,
            'history': conversation_history[session_id]
        })
    return jsonify({'success': True, 'history': []})

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'engine': 'EnhancedAI',
        'features': ['courses', 'games', 'assessments', 'disability_info', 'tips', 'facts'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/get-tip', methods=['GET'])
def get_tip():
    """Get a random learning tip"""
    tip = random.choice(ai_engine.learning_tips)
    return jsonify({'success': True, 'tip': tip})

@app.route('/api/get-fact', methods=['GET'])
def get_fact():
    """Get a random fun fact"""
    fact = random.choice(ai_engine.fun_facts)
    return jsonify({'success': True, 'fact': fact})

@app.route('/api/session/<session_id>', methods=['DELETE'])
def clear_session(session_id):
    """Clear conversation history"""
    if session_id in conversation_history:
        del conversation_history[session_id]
    if session_id in ai_engine.last_intent:
        del ai_engine.last_intent[session_id]
    return jsonify({'success': True, 'message': 'Session cleared'})

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧠 Bright Minds - Enhanced AI Learning Platform")
    print("="*60)
    print("✨ Features:")
    print("   • Course recommendations with direct links")
    print("   • Quiz links that open assessment page")
    print("   • Game links for interactive learning")
    print("   • Context-aware conversations")
    print("   • Mood detection and responses")
    print("\n🚀 Server running at: http://localhost:5000")
    print("📱 Open this URL in your browser")
    print("⚠️  Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)