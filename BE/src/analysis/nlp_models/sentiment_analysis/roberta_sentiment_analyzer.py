from scipy.special import softmax
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

MODEL = f"cardiffnlp/twitter-xlm-roberta-base-sentiment"


def analyze_sentiment(text: str) -> float:
    tokenizer = AutoTokenizer.from_pretrained(MODEL, use_fast=False)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    mappings = {"Negative": scores[0], "Neutral": scores[1], "Positive": scores[2]}

    max_score = max(mappings.values())

    key_val = ""
    for key in mappings:
        if mappings[key] == max_score:
            key_val = key

    # "normalize" results according to use by this program
    if key_val == "Negative":
        max_score = -max_score
    elif key_val == "Neutral":
        max_score = 0.0

    return max_score


if __name__ == '__main__':
    example_sentence = "Im Moment ist mein Alltag eher eintönig, da mein Mann für Ausflüge zu wenig mobil ist. "
    print(analyze_sentiment(example_sentence))
