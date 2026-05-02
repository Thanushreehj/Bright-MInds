# config/settings.py - Configuration settings for Bright Minds

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / 'backend'
FRONTEND_DIR = BASE_DIR / 'frontend'
DATA_DIR = BASE_DIR / 'data'
MODELS_DIR = BACKEND_DIR / 'models'

# Create directories if they don't exist
for dir_path in [DATA_DIR, MODELS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# AI Model settings
AI_MODEL_NAME = 'all-MiniLM-L6-v2'
AI_MODEL_CACHE_DIR = str(MODELS_DIR)
AI_CONFIDENCE_THRESHOLD = 0.3

# Server settings
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG_MODE = True

# API settings
API_BASE_URL = f'http://localhost:{SERVER_PORT}/api'
CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000', 'http://127.0.0.1:5000']

# Session settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MAX_HISTORY_PER_SESSION = 20

# Quiz settings
DEFAULT_QUIZ_QUESTIONS = 10
DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']
SCORE_THRESHOLDS = {
    'excellent': 90,
    'good': 70,
    'average': 50,
    'needs_improvement': 30
}

# Learning styles
LEARNING_STYLES = {
    'visual': {
        'name': 'Visual Learner',
        'icon': '👁️',
        'description': 'Learn best by seeing and observing',
        'strategies': ['Use diagrams', 'Watch videos', 'Color code notes']
    },
    'auditory': {
        'name': 'Auditory Learner',
        'icon': '👂',
        'description': 'Learn best by listening',
        'strategies': ['Read aloud', 'Use rhymes', 'Discuss topics']
    },
    'kinesthetic': {
        'name': 'Kinesthetic Learner',
        'icon': '✋',
        'description': 'Learn best by doing',
        'strategies': ['Hands-on activities', 'Take breaks', 'Role play']
    }
}

# Game settings
GAMES_CONFIG = {
    'memory': {
        'grid_size': 4,
        'pairs': 8,
        'time_limit': 60  # seconds
    },
    'word_scramble': {
        'words_per_session': 10,
        'time_per_word': 30
    },
    'pattern': {
        'levels': 10,
        'difficulty_progression': True
    }
}

# Disability awareness resources
DISABILITY_RESOURCES = {
    'adhd': {
        'name': 'ADHD',
        'color': '#FF9A3C',
        'symptoms': ['Inattention', 'Hyperactivity', 'Impulsivity'],
        'strategies': ['Short tasks', 'Frequent breaks', 'Visual schedules']
    },
    'autism': {
        'name': 'Autism Spectrum Disorder',
        'color': '#6C63FF',
        'symptoms': ['Social challenges', 'Sensory sensitivities', 'Routine preference'],
        'strategies': ['Structured environment', 'Visual supports', 'Sensory breaks']
    },
    'dyslexia': {
        'name': 'Dyslexia',
        'color': '#4ECDC4',
        'symptoms': ['Reading difficulty', 'Spelling challenges', 'Letter reversal'],
        'strategies': ['Multi-sensory learning', 'Audio support', 'Decodable text']
    },
    'slow_learning': {
        'name': 'Slow Learning',
        'color': '#6BCB77',
        'symptoms': ['Slower pace', 'Need repetition', 'Difficulty with abstractions'],
        'strategies': ['Extra time', 'Step-by-step', 'Concrete examples']
    }
}

# Email settings (if you add email feature)
EMAIL_CONFIG = {
    'enabled': False,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '',
    'sender_password': ''
}

# Logging settings
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

def get_setting(key, default=None):
    """Get a setting value, with optional environment variable override"""
    env_key = f'BRIGHTMINDS_{key.upper()}'
    return os.environ.get(env_key, globals().get(key, default))

# Load environment variables if .env file exists
try:
    from dotenv import load_dotenv
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded environment variables from {env_file}")
except ImportError:
    pass