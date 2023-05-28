"""
Function to calculate precision, recall, F1 score after performing evaluation tests.
"""
import csv
import os

from BE.src.DTOs.topicSentimentDTO import AvgTopicSentimentDTO
from BE.src.db_handling.populate_database.utility import DELIMITER
from BE.src.preprocessing.lemmatizer import lemmatize_sentence

# change cwd for reading files more easily
project_root = "BE"
while True:
    if project_root in os.listdir():
        break
    os.chdir('..')

eval_results_path = "Data/evaluation/results/eval_results-huggingface_multi.csv"

eval_solution_path = "Data/evaluation/eval_results-SOLUTION.csv"

all_correct_topics = []


def parse_results(filename: str) -> dict[str, list[AvgTopicSentimentDTO]]:
    results = {}

    with open(filename) as file:
        reader = csv.reader(file)
        # skip header row
        next(reader)

        curr_key = "ERROR"
        for row in reader:
            if row[1] == DELIMITER:
                curr_key = row[0]
                results[curr_key] = []
            else:
                # parse found topic
                r = AvgTopicSentimentDTO(
                    topic=row[0],
                    overall_sentiment=row[1],
                    patient_id=1,  # doesn't matter
                    nr_of_occurrences=1  # doesn't matter
                )
                if curr_key in results:
                    results[curr_key].append(r)
                else:
                    raise Exception("Key error when parsing .csv file")

        return results


def calculate_accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    return (tp + tn) / (tp + tn + fp + fn)


def calculate_precision(tp: int, fp: int) -> float:
    return tp / (tp + fp)


def calculate_recall(tp: int, fn: int) -> float:
    return tp / (tp + fn)


def calculate_f1(precision: float, recall: float) -> float:
    return 2 * ((precision * recall) / (precision + recall))


actual = parse_results(eval_results_path)

expected = parse_results(eval_solution_path)

total_topics = 0

total_sentiments = 0

total_tp_topics = []

confusion_matrix_topics = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

confusion_matrix_sentiments = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

# calculate confusion matrix values
for key, expected_vals in expected.items():

    result_vals = actual[key]

    result_topics = [r.topic.strip() for r in result_vals]

    expected_topics = [r.topic.strip() for r in expected_vals]

    tp_topics = []

    # calculate true positives and false negatives
    for e in expected_topics:
        total_topics += 1
        if e in result_topics:
            confusion_matrix_topics["TP"] += 1
            tp_topics.append(e)
            total_tp_topics.append(e)
        else:
            confusion_matrix_topics["FN"] += 1

    # calculate false positives
    for result in result_topics:
        if result not in expected_topics:
            confusion_matrix_topics["FP"] += 1

    # gather topics we want to use for sentiment analysis metrics
    for e in expected_vals:
        if e.overall_sentiment == "Neutral" and e.topic in tp_topics:
            tp_topics.remove(e.topic)

    total_sentiments += len(tp_topics)

    # calculate sentiment  confusion matrix
    for e in result_vals:
        if e.topic in tp_topics:
            expected_dto = next((x for x in expected_vals if x.topic == e.topic), None)
            if e.overall_sentiment == "Positive" and expected_dto.overall_sentiment == "Positive":
                confusion_matrix_sentiments["TP"] += 1
            elif e.overall_sentiment == "Negative" and expected_dto.overall_sentiment == "Negative":
                confusion_matrix_sentiments["TN"] += 1
            elif expected_dto.overall_sentiment == "Negative" and (e.overall_sentiment == "Positive" or e.overall_sentiment == "Neutral"):
                confusion_matrix_sentiments["FP"] += 1
            elif expected_dto.overall_sentiment == "Positive" and (e.overall_sentiment == "Negative" or e.overall_sentiment == "Neutral"):
                confusion_matrix_sentiments["FN"] += 1

print("\n### Confusion Matrix Topic Detection ###".upper())
print(f"\nTotal topics to be found: {total_topics}")
for key, val in confusion_matrix_topics.items():
    print(f"{key}:\t{val}")

# calculate topic detection metrics
topic_detection_precision = calculate_precision(confusion_matrix_topics["TP"], confusion_matrix_topics["FP"])
topic_detection_recall = calculate_recall(confusion_matrix_topics["TP"], confusion_matrix_topics["FN"])
topics_detection_f1 = calculate_f1(topic_detection_precision, topic_detection_recall)

print(f"\nPrecision:\t{topic_detection_precision}")
print(f"Recall:\t\t{topic_detection_recall}")
print(f"F1:\t\t\t{topics_detection_f1}")

print("\n### Confusion Matrix Sentiment Analysis ###".upper())
print(f"Total sentiments to be found: {total_sentiments}")
for key, val in confusion_matrix_sentiments.items():
    print(f"{key}:\t{val}")

# calculate sentiment analysis metrics
sentiment_detection_accuracy = calculate_accuracy(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["TN"], confusion_matrix_sentiments["FP"], confusion_matrix_sentiments["FN"])
sentiment_detection_precision = calculate_precision(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["FP"])
sentiment_detection_recall = calculate_recall(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["FN"])
sentiments_detection_f1 = calculate_f1(sentiment_detection_precision, sentiment_detection_recall)

#  print(f"True positives topics: {total_tp_topics}")

print(f"Accurcay:\t{sentiment_detection_accuracy}")
print(f"Precision:\t{sentiment_detection_precision}")
print(f"Recall:\t\t{sentiment_detection_recall}")
print(f"F1:\t\t\t{sentiments_detection_f1}")
