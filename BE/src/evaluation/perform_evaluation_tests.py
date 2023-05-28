import csv

from BE.src.analysis.nlp_models.absa.absa_huggingface import absa_huggingface
from BE.src.analysis.nlp_models.absa.absa_simple import aspect_sentiment_analysis
from BE.src.analysis.topic_based_sentiment_analyzer import topic_based_sentiment_analysis
from BE.src.config import config_instance
from BE.src.db_handling.populate_database.utility import DELIMITER
from BE.src.preprocessing.data_cleaner import clean_sentences
from BE.src.preprocessing.data_loader import parse_file_lines

# load data
path = config_instance.raw_data_path
data = parse_file_lines(path)
data = [entry.text_entry for entry in data]


def write_results_to_file(output_filename: str, input_data: list[str], model_name="tbsa") -> None:
    """
    For the evaluation of the engine we process the entries multiple times by various models.
    With the use of this function we can simplify that process and keep the code cleaner.
    """
    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # header row
        writer.writerow(['Topic', 'Sentiment', 'Polarity'])

        for entry in input_data:
            writer.writerow([entry, DELIMITER, DELIMITER])

            # get results from desired analysis function
            if model_name == "huggingface_multi":
                results = absa_huggingface(entry)
            elif model_name == "huggingface_en":
                results = absa_huggingface(entry, "english")
            elif model_name == "absa":
                results = aspect_sentiment_analysis(entry)
            else:
                results = topic_based_sentiment_analysis(entry)

            for r in results:
                if r.sentiment >= 0.2:
                    sentiment = "Positive"
                elif r.sentiment <= -0.2:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

                row = [r.topic, sentiment, r.sentiment]
                writer.writerow(row)


folder_path = "Data/evaluation/results"
test_nr = "06"

# # get engine's topic based sentiment detection's results
# filename = f"{folder_path}/{test_nr}-eval_results-TBSA.csv"
# write_results_to_file(filename, data)

# # get engine's pure ABSA results
# filename = f"{folder_path}/{test_nr}-eval_results-ABSA.csv"
# write_results_to_file(filename, data, "absa")

# get hugging face's ABSA results (multilingual)
filename = f"{folder_path}/{test_nr}-eval_results-huggingface_multi.csv"
write_results_to_file(filename, data, "huggingface_multi")

# get hugging face's ABSA results (English)
filename = f"{folder_path}/{test_nr}-eval_results-huggingface_en.csv"
write_results_to_file(filename, data, "huggingface_en")
