from spellchecker import SpellChecker

# TODO: try textblob spellchecker?


def check_spelling(sentence: str, lang="de"):
    spell = SpellChecker(language=lang)
    words = sentence.split()
    words = [w.lower() for w in words]
    misspelled = spell.unknown(words)

    corrections = {}
    for word in misspelled:
        corrected_w = spell.correction(word)
        if corrected_w is not None:
            corrections[word] = spell.correction(word)
        else:
            corrections[word] = word

    result = ""
    for word in words:
        if word in corrections.keys():
            result += corrections[word] + " "
        else:
            result += word + " "

    return result


if __name__ == '__main__':
    example_sentence = "sandwich vegetarisch tommoz plus Berliner"
    print(check_spelling(example_sentence))
