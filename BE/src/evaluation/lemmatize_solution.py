import csv

from BE.src.db_handling.populate_database.utility import DELIMITER
from BE.src.preprocessing.lemmatizer import lemmatize_sentence

file_path = "Data/evaluation/eval_results-SOLUTION.csv"

accepted_sentiments = ["Negative", "Positive", "Neutral"]

# Read original lines
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    original_rows = list(reader)

modified_rows = []

# Control and correct lines where needed
for idx, row in enumerate(original_rows):
    if idx != 0:
        if row[1] != DELIMITER:
            # lemmatize topic name
            topic = lemmatize_sentence(row[0])
            row[0] = topic

            # control sentiment labeling
            if row[1] not in accepted_sentiments:
                raise Exception(f"Wrong value for sentiment '{row[1]}'. Please correct .csv file.")

    modified_rows.append(row)


# Write changes back to the file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(modified_rows)
