"""
Utility function to translate text with DeepL API for use with the models that only accept English input.
"""

import deepl

from BE.src.config import config_instance


def translate(sentence: str, lang="EN-US") -> str:

    translator = deepl.Translator(config_instance.deepl_api_key)

    result = translator.translate_text(sentence, target_lang=lang)

    return result.text


if __name__ == '__main__':
    example = """
    Wir haben Gäste Abends und bekochen sie. 19.00 h Apéro 2 dl Weisswein, 19.30 h selbstgemachte Kürbissuppe, 1/2 
    Kürbisbrötchen, 2 dl Rotwein, 5 dl Mineralwasser, Thaicurry mit Reis, Crema Catalana mit Blutorangen und Rahm
    """
    print(translate(example))
