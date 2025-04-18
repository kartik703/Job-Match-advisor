from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang='en'):
    if target_lang.lower() == 'english':
        return text
    try:
        translation = translator.translate(text, dest=lang_code(target_lang))
        return translation.text
    except Exception as e:
        return text  # fallback if API fails

def lang_code(language):
    lang_map = {
        'english': 'en',
        'spanish': 'es',
        'french': 'fr',
        'german': 'de',
        'hindi': 'hi',
        'chinese': 'zh-cn'
    }
    return lang_map.get(language.lower(), 'en')
