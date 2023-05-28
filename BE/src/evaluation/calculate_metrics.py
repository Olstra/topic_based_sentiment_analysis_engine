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

eval_results_path = "Data/evaluation/results/05-eval_results-huggingface_multi.csv"

eval_solution_path = "Data/evaluation/04-eval_results-SOLUTION.csv"


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


actual_results = parse_results(eval_results_path)

expected = parse_results(eval_solution_path)

total_topics = 0
confusion_matrix_topics = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
confusion_matrix_sentiments = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}
true_positives = []

# calculate confusion matrix values
for key, expected_vals in expected.items():

    result_vals = actual_results[key]

    # TODO remove lemmatizing here after getting test results nr 6
    result_topics = [lemmatize_sentence(r.topic.strip()) for r in result_vals]

    # lemmatize human annotated results
    expected_topics = [lemmatize_sentence(r.topic.strip()) for r in expected_vals]

    tp_topics = []

    # calculate true positives and false negatives
    for e in expected_topics:
        total_topics += 1
        if e in result_topics:
            confusion_matrix_topics["TP"] += 1
            true_positives.append(e)
        else:
            confusion_matrix_topics["FN"] += 1

    # calculate false positives
    for result in result_topics:
        if result not in expected_topics:
            confusion_matrix_topics["FP"] += 1

    # calculate sentiments

print("Confusion Matrix Topic Detection")
print(f"Total topics to be found: {total_topics}")
for key, val in confusion_matrix_topics.items():
    print(f"{key}:\t{val}")

# calculate topic detection metrics
topic_detection_accuracy = calculate_accuracy(confusion_matrix_topics["TP"], confusion_matrix_topics["TN"], confusion_matrix_topics["FP"], confusion_matrix_topics["FN"])
topic_detection_precision = calculate_precision(confusion_matrix_topics["TP"], confusion_matrix_topics["FP"])
topic_detection_recall = calculate_recall(confusion_matrix_topics["TP"], confusion_matrix_topics["FN"])
topics_detection_f1 = calculate_f1(topic_detection_precision, topic_detection_recall)

print(f"Accurcay:\t{topic_detection_accuracy}"
      f"\nPrecision:\t{topic_detection_precision}"
      f"\nRecall:\t\t{topic_detection_recall}"
      f"\nF1:\t\t{topics_detection_f1}")

print("Confusion Matrix Sentiment Analysis")
print(f"Total sentiments to be found: {0}")  # todo add total sents
for key, val in confusion_matrix_sentiments.items():
    print(f"{key}:\t{val}")

# # calculate sentiment analysis metrics
# sentiment_detection_accuracy = calculate_accuracy(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["TN"], confusion_matrix_sentiments["FP"], confusion_matrix_sentiments["FN"])
# sentiment_detection_precision = calculate_precision(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["FP"])
# sentiment_detection_recall = calculate_recall(confusion_matrix_sentiments["TP"], confusion_matrix_sentiments["FN"])
# sentiments_detection_f1 = calculate_f1(sentiment_detection_precision, sentiment_detection_recall)

print(f"True positives: {true_positives}")

# print(f"Accurcay:\t{sentiment_detection_accuracy}"
#       f"Precision:\t{sentiment_detection_precision}"
#       f"Recall:\t{sentiment_detection_recall}"
#       f"F1:\t{sentiments_detection_f1}")
