# backend/simple_ai.py - Simplified AI Engine (No external ML dependencies)

import json
import random
import re
from difflib import SequenceMatcher

class SimpleAI:
    """Simple but effective rule-based AI with fuzzy matching"""
    
    def __init__(self):
        self.intents = {}
        self.responses = {}
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load knowledge base"""
        
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
            'quiz': ['quiz', 'test', 'assessment', 'exam', 'practice', 'challenge'],
            'tip': ['tip', 'advice', 'strategy', 'how to study', 'remember', 'technique'],
            'fact': ['fact', 'did you know', 'interesting', 'surprise me', 'tell me something'],
            'help': ['help', 'what can you do', 'support', 'guide', 'tutorial']
        }
        
        # Responses
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
                "📚 **Bright Minds Courses:**\n\n🔢 **Mathematics** - Numbers, addition, subtraction, multiplication, word problems\n📖 **English** - Grammar, vocabulary, reading comprehension\n🌍 **General Knowledge** - Science, geography, animals, fun facts\n\nWhich subject interests you most?"
            ],
            'math': [
                "➕ **Math at Bright Minds** includes:\n\n• Counting and number recognition\n• Addition & subtraction with visuals\n• Multiplication tables\n• Word problems\n• Fractions and geometry\n\nWant to try a math quiz? 🎯"
            ],
            'english': [
                "📖 **English Learning** at Bright Minds:\n\n• Alphabet & phonics\n• Sight words and vocabulary\n• Grammar: nouns, verbs, adjectives\n• Sentence construction\n• Reading comprehension\n\nReady for an English challenge? 📝"
            ],
            'gk': [
                "🌍 **General Knowledge** topics:\n\n• Animals and their habitats 🦁\n• Solar system and space 🌟\n• Countries and capitals 🗺️\n• Science facts 🔬\n• Famous inventors 💡\n\nWant a fun GK fact?"
            ],
            'adhd': [
                "💡 **ADHD (Attention Deficit Hyperactivity Disorder)** affects focus, impulse control, and activity levels.\n\n**How Bright Minds helps:**\n✓ Short, engaging activities (10-15 min)\n✓ Immediate feedback and rewards\n✓ Minimized distractions\n✓ Break tasks into small steps\n\nWould you like learning strategies for ADHD? 🎯"
            ],
            'autism': [
                "💙 **Autism Spectrum Disorder (ASD)** affects communication and sensory processing.\n\n**Bright Minds features:**\n✓ Predictable, structured lessons\n✓ Visual learning emphasis\n✓ Calm, low-stimulation design\n✓ Option to repeat and review\n\nWould you like tips for supporting an autistic learner? 🤗"
            ],
            'dyslexia': [
                "📝 **Dyslexia** affects reading, spelling, and writing — but NOT intelligence!\n\n**How we help:**\n✓ Multi-sensory learning\n✓ Readable fonts and colors\n✓ Audio support\n✓ Word games\n\nWant to try our word games? 🎮"
            ],
            'games': [
                "🎮 **Available Games:**\n\n🃏 **Memory Match** - Build focus and memory\n🔤 **Word Scramble** - Improve spelling\n🔢 **Pattern Play** - Develop thinking skills\n\nWhich game would you like to play? 🎯"
            ],
            'quiz': [
                "📝 **Ready to test your knowledge?**\n\nTake our AI-powered assessment:\n• Adaptive questions\n• Instant scoring\n• Personalized feedback\n\nClick 'AI Assessment' in the menu to start! 🎯"
            ],
            'tip': [
                "💡 **Learning Tip:**\n\nTry the Pomodoro technique: Study for 15 minutes, then take a 5-minute break. It's great for maintaining focus!\n\nWant another tip? 🌟"
            ],
            'fact': [
                "🌟 **Did you know?**\n\n🐙 An octopus has THREE hearts! Two pump blood to the gills, and one pumps it to the rest of the body!\n\nWant another fun fact? 🎉"
            ],
            'help': [
                "🆘 **I can help you with:**\n\n📚 Courses (Math, English, GK)\n🎮 Games and activities\n🧠 ADHD, Autism, Dyslexia\n📝 Quizzes and assessments\n💡 Learning tips and fun facts\n\nWhat would you like to know?"
            ],
            'default': [
                "🤔 I'm not sure about that. Could you rephrase?\n\n**I can help with:**\n• 📚 Courses\n• 🎮 Games\n• 🧠 ADHD/Autism info\n• 💡 Learning tips\n\nWhat would you like to know?"
            ]
        }
        
        # Dynamic content
        self.learning_tips = [
            "🎯 **Pomodoro Technique:** Study 15 min, break 5 min",
            "🎵 **Music helps memory:** Sing spelling words to a tune!",
            "🎨 **Color coding:** Use different colors for different subjects",
            "🧘 **Deep breaths:** 3 deep breaths before studying improves focus",
            "⭐ **Celebrate small wins:** Every step forward counts!",
            "🔄 **Review:** Spend 5 minutes reviewing yesterday's lesson",
            "🎮 **Gamify:** Turn practice into a game with timers",
            "📖 **Read aloud:** Helps with comprehension and focus"
        ]
        
        self.fun_facts = [
            "🐙 Octopuses have THREE hearts!",
            "🍯 Honey never expires - it can last forever!",
            "🐘 Elephants are the only mammals that can't jump",
            "🌍 Earth is the only planet not named after a god",
            "🦋 A group of flamingos is called a 'flamboyance'",
            "📚 The word 'school' originally meant 'leisure'",
            "🌱 A tree can absorb 48 lbs of CO2 per year!",
            "🐧 Penguins propose with a pebble!"
        ]
        
        # Mood responses
        self.mood_responses = {
            'happy': "😊 That's wonderful! A happy mind learns best!",
            'excited': "🤩 I love your energy! Let's learn something amazing!",
            'calm': "😌 A calm mind is perfect for focused study!",
            'tired': "😴 Let's start with something light and easy!",
            'confused': "😕 No worries! Let's figure this out together!",
            'sad': "💛 I'm here for you. Let's do something gentle today."
        }
    
    def get_similarity(self, a, b):
        """Calculate string similarity"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    def match_intent(self, text):
        """Match user input to closest intent"""
        text_lower = text.lower()
        
        # Check for mood first
        mood = self.detect_mood(text_lower)
        if mood:
            return 'mood', mood
        
        # Score each intent
        scores = {}
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                # Check for partial matches
                if len(keyword) > 3 and keyword in text_lower:
                    score += 0.5
            scores[intent] = score
        
        # Get best match
        if scores:
            best_intent = max(scores, key=scores.get)
            best_score = scores[best_intent]
            if best_score > 0:
                return best_intent, best_score
        
        return 'help', 0
    
    def detect_mood(self, text):
        """Detect mood from text"""
        mood_map = {
            'happy': ['happy', 'great', 'wonderful', 'good', 'fantastic', 'awesome'],
            'excited': ['excited', 'thrilled', 'pumped', 'energized'],
            'calm': ['calm', 'relaxed', 'peaceful', 'chill'],
            'tired': ['tired', 'sleepy', 'exhausted', 'drained'],
            'confused': ['confused', 'puzzled', 'lost', 'unclear'],
            'sad': ['sad', 'down', 'unhappy', 'depressed']
        }
        
        for mood, keywords in mood_map.items():
            for keyword in keywords:
                if keyword in text:
                    return mood
        return None
    
    def get_response(self, intent, mood=None):
        """Get response based on intent"""
        import random
        
        if intent == 'mood' and mood:
            return self.mood_responses.get(mood, "😊 Thanks for sharing!")
        
        if intent == 'tip':
            tip = random.choice(self.learning_tips)
            return f"💡 **Learning Tip:**\n\n{tip}\n\nWould you like another tip?"
        
        if intent == 'fact':
            fact = random.choice(self.fun_facts)
            return f"🌟 **Did you know?**\n\n{fact}\n\nWant another fun fact?"
        
        responses = self.responses.get(intent, self.responses['default'])
        return random.choice(responses)
    
    def get_suggestions(self, intent):
        """Get follow-up suggestions"""
        suggestions_map = {
            'greet': ['Tell me about courses', 'What games can I play?', 'Give me a tip'],
            'courses': ['Tell me about Math', 'Tell me about English', 'Take a quiz'],
            'math': ['Practice math', 'Take math quiz', 'Tell me about English'],
            'english': ['Practice spelling', 'Take English quiz', 'Tell me about GK'],
            'adhd': ['ADHD learning tips', 'ADHD games', 'Talk about Autism'],
            'autism': ['Autism learning tips', 'Calming activities', 'Talk about ADHD'],
            'games': ['Memory match', 'Word scramble', 'Pattern game'],
            'quiz': ['Take assessment', 'Practice questions', 'Tell me about courses'],
            'default': ['Show me courses', 'Give me a tip', 'Tell me a fact']
        }
        
        suggestions = suggestions_map.get(intent, suggestions_map['default'])
        return suggestions[:4]  # Return top 4 suggestions