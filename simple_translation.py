"""
Simple translation utility for common phrases
"""

TRANSLATION_DICT = {
    'hi-IN': {
        'नमस्ते': 'Hello',
        'धन्यवाद': 'Thank you',
        'कैसे हैं आप': 'How are you',
        'मेरा नाम': 'My name is',
        'आप कैसे हैं': 'How are you',
        'क्या हाल है': 'What\'s up',
        'अच्छा': 'Good',
        'बुरा': 'Bad',
        'हाँ': 'Yes',
        'नहीं': 'No'
    },
    'te-IN': {
        'నమస్కారం': 'Hello',
        'ధన్యవాదాలు': 'Thank you',
        'మీరు ఎలా ఉన్నారు': 'How are you',
        'నా పేరు': 'My name is',
        'హసిని': 'Hasini',
        'పుత్తూర్': 'Puttur',
        'ఉన్నాను': 'I am',
        'నేను': 'I',
        'మంచిది': 'Good',
        'చెడు': 'Bad',
        'అవును': 'Yes',
        'కాదు': 'No'
    },
    'ta-IN': {
        'வணக்கம்': 'Hello',
        'நன்றி': 'Thank you',
        'நீங்கள் எப்படி இருக்கிறீர்கள்': 'How are you',
        'என் பெயர்': 'My name is',
        'நல்லது': 'Good',
        'கெட்டது': 'Bad',
        'ஆம்': 'Yes',
        'இல்லை': 'No'
    },
    'bn-IN': {
        'নমস্কার': 'Hello',
        'ধন্যবাদ': 'Thank you',
        'আপনি কেমন আছেন': 'How are you',
        'আমার নাম': 'My name is',
        'ভালো': 'Good',
        'খারাপ': 'Bad',
        'হ্যাঁ': 'Yes',
        'না': 'No'
    },
    'gu-IN': {
        'નમસ્તે': 'Hello',
        'આભાર': 'Thank you',
        'તમે કેમ છો': 'How are you',
        'મારું નામ': 'My name is',
        'સારું': 'Good',
        'ખરાબ': 'Bad',
        'હા': 'Yes',
        'ના': 'No'
    }
}

def simple_translate(text, source_language):
    """
    Simple translation using dictionary lookup
    """
    if source_language not in TRANSLATION_DICT:
        return f"{text} (Translation not available for {source_language})"
    
    translations = TRANSLATION_DICT[source_language]
    translated_text = text
    
    # Replace known phrases
    for original, english in translations.items():
        if original in text:
            translated_text = translated_text.replace(original, english)
    
    # If any translation was made, mark it
    if translated_text != text:
        return f"{translated_text} (Partial translation)"
    else:
        return f"{text} (No translation available)"

def get_language_name(language_code):
    """Get human readable language name"""
    language_names = {
        'hi-IN': 'Hindi',
        'te-IN': 'Telugu', 
        'ta-IN': 'Tamil',
        'bn-IN': 'Bengali',
        'gu-IN': 'Gujarati',
        'kn-IN': 'Kannada',
        'ml-IN': 'Malayalam',
        'mr-IN': 'Marathi',
        'pa-IN': 'Punjabi',
        'od-IN': 'Odia',
        'en-IN': 'English'
    }
    return language_names.get(language_code, language_code)
