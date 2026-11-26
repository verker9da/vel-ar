"""VELOCITY JAPANESE - language pack, brand and motion design constants."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_DIR = BASE_DIR / "output"
LESSONS_DIR = OUTPUT_DIR / "lessons"
HISTORY_DIR = OUTPUT_DIR / "history"
SCENE_DIR = BASE_DIR / "scene"

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# ---------------------------------------------------------------- brand

BRAND = "VELOCITY ARABIC"
BRAND_LOCKUP_TOP = "VELOCITY"
BRAND_LOCKUP_BOTTOM = "ARABIC"
HANDLE = "@velocityarabic"
MASCOT_NAME = "Velo"

# ==== LANGUAGE PACK START ====
LANGUAGE = {
    "code": "ar",
    "name": "Arabic",
    "native_name": "العربية",
    "history_key": "arabic",
    "english_voice": "en-US-AvaNeural",
    "english_fallback_voice": "en-US-GuyNeural",
    "native_voice": "ar-SA-ZariyahNeural",
    "native_fallback_voice": "ar-SA-HamedNeural",
    "native_engine": "edge",
    "native_lang_code": "ar",
    "english_rate": "-4%",
    "native_rate": "-10%",
    "english_pitch": "+0Hz",
    "native_pitch": "+0Hz",
    "native_label": "العربية",
    "translit_label": "SAY IT LIKE",
    "flag": "sa",
    "greeting": "مرحباً!",
    "encouragement": "ممتاز!",
    "rtl": True,
    "char_tiles": False,
    "script_font": "NotoSansArabic-Bold.ttf",
    "glyphs": "أبتثجحخدذرزسشصضطظعغفقكلمنهوي",
}
# ==== LANGUAGE PACK END ====

AI_MODEL = os.getenv("AI_MODEL", "gemini-fast")
POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "")

# ---------------------------------------------------------------- timing (seconds)

INTRO_DURATION = 4.0
OUTRO_DURATION = 5.2
EN_CARD_IN = 0.55
GAP_EN_NATIVE = 0.5
NATIVE_CARD_LEAD = 0.35
GAP_BEFORE_REPEAT = 0.8
TAIL_HOLD = 1.4
MAX_REEL_DURATION = 88.0

# ---------------------------------------------------------------- palette

INK = "#3C3C3C"
MUTED = "#8A8A8A"
CREAM = "#FFF8E7"
GREEN = "#58CC02"
GREEN_DARK = "#46A302"
GREEN_DEEP = "#3D8F00"
BLUE = "#1CB0F6"
PURPLE = "#A560E8"
ORANGE = "#FF7A00"
RED = "#FF4B4B"
YELLOW = "#F5A700"
TEAL = "#00A889"
PINK = "#E056A0"

PALETTE = [GREEN, BLUE, PURPLE, ORANGE, RED, YELLOW, TEAL, PINK]

# ---------------------------------------------------------------- categories
# (english, native, icon, accent)

# ==== CATEGORY TABLE START ====
CATEGORY_TABLE = [
    ("Greetings", "تحيات", "hand", "#1CB0F6"),
    ("Basic Phrases", "عبارات أساسية", "chat", "#58CC02"),
    ("Common Expressions", "تعبيرات شائعة", "chat", "#1CB0F6"),
    ("Travel", "السفر", "plane", "#1CB0F6"),
    ("Restaurant", "مطعم", "fork", "#FF7A00"),
    ("Shopping", "التسوق", "bag", "#E056A0"),
    ("Emergency", "الطوارئ", "siren", "#FF4B4B"),
    ("Family Terms", "أفراد الأسرة", "heart", "#E056A0"),
    ("Numbers", "الأرقام", "hash", "#A560E8"),
    ("Time", "الوقت", "clock", "#00A889"),
    ("Motivation", "التحفيز", "rocket", "#A560E8"),
    ("Love", "الحب", "heart", "#FF4B4B"),
    ("Success", "النجاح", "trophy", "#F5A700"),
    ("Wisdom", "الحكمة", "book", "#A560E8"),
    ("Happiness", "السعادة", "smile", "#F5A700"),
    ("Self Improvement", "تطوير الذات", "leaf", "#58CC02"),
    ("Gratitude", "الامتنان", "heart", "#FF7A00"),
    ("Friendship", "الصداقة", "users", "#00A889"),
    ("Hope", "الأمل", "sun", "#FF7A00"),
    ("Creativity", "الإبداع", "palette", "#E056A0"),
    ("Inner Peace", "السلام الداخلي", "lotus", "#00A889"),
    ("Confidence", "الثقة", "shield", "#1CB0F6"),
    ("Perseverance", "المثابرة", "mountain", "#FF7A00"),
    ("Inspiration", "الإلهام", "sparkles", "#A560E8"),
    ("Positive Life", "حياة إيجابية", "sun", "#58CC02"),
    ("Courage", "الشجاعة", "shield", "#FF4B4B"),
    ("Kindness", "اللطف", "heart", "#E056A0"),
    ("Patience", "الصبر", "hourglass", "#00A889"),
    ("Forgiveness", "التسامح", "hands", "#FF7A00"),
    ("Strength", "القوة", "dumbbell", "#FF4B4B"),
    ("Joy", "الفرح", "smile", "#F5A700"),
    ("Balance", "التوازن", "scale", "#00A889"),
    ("Growth", "النمو", "sprout", "#58CC02"),
    ("Purpose", "الهدف", "target", "#A560E8"),
    ("Mindfulness", "اليقظة الذهنية", "lotus", "#00A889"),
    ("Daily Routine", "الروتين اليومي", "calendar", "#1CB0F6"),
    ("Weather", "الطقس", "cloud", "#1CB0F6"),
    ("Feelings", "المشاعر", "smile", "#E056A0"),
    ("Food", "الطعام", "fork", "#FF7A00"),
    ("Health", "الصحة", "heart", "#58CC02"),
    ("Work", "العمل", "briefcase", "#1CB0F6"),
    ("Technology", "التكنولوجيا", "chip", "#A560E8"),
    ("Nature", "الطبيعة", "leaf", "#58CC02"),
    ("Animals", "الحيوانات", "paw", "#FF7A00"),
    ("Colors", "الألوان", "palette", "#E056A0"),
    ("Directions", "الاتجاهات", "compass", "#1CB0F6"),
    ("Body Parts", "أجزاء الجسم", "hand", "#00A889"),
    ("Clothes", "الملابس", "shirt", "#E056A0"),
    ("Music", "الموسيقى", "music", "#A560E8"),
    ("Sports", "الرياضة", "ball", "#FF7A00"),
    ("Holidays", "العطلات", "gift", "#FF4B4B"),
    ("Education", "التعليم", "book", "#1CB0F6"),
    ("Culture", "الثقافة", "globe", "#00A889"),
    ("Finance", "المال", "coin", "#58CC02"),
    ("Relationships", "العلاقات", "users", "#E056A0"),
]
# ==== CATEGORY TABLE END ====

CATEGORIES = [c[0] for c in CATEGORY_TABLE]
CATEGORIES_NATIVE = {c[0]: c[1] for c in CATEGORY_TABLE}
CATEGORY_META = {c[0]: {"native": c[1], "icon": c[2], "accent": c[3]} for c in CATEGORY_TABLE}
MAX_RECENT_CATEGORIES = 25

# ==== HASHTAGS START ====
HASHTAGS = [
    "#learnarabic",
    "#arabiclessons",
    "#arabicforbeginners",
    "#languagelearning",
    "#arabicvocabulary",
    "#velocityarabic",
    "#dailyarabic",
    "#arabic",
    "#learnlanguages",
    "#speakarabic",
    "#bilingual",
    "#languagetips",
]
# ==== HASHTAGS END ====
