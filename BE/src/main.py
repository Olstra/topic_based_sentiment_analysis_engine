"""
The API of our engine.
"""
from flask import Flask, jsonify, Response

from BE.src.analysis.openai_model.openai_model import OpenaiModel
from BE.src.analysis.legacy_wordcloud.valence_entries_parser import parse_valence_entries, parse_valence_datasets
from BE.src.config import config_instance
from BE.src.db_handling.db_handler import db_handler

model = OpenaiModel()

app = Flask(__name__)


@app.route('/journal-entries/<string:patient_id>', methods=['GET'])
def get_patient_journal_entries(patient_id):
    entries = db_handler.get_patient_summaries(patient_id)
    return jsonify(entries)


@app.route('/mood-entries/<string:patient_id>', methods=['GET'])
def get_patient_mood_entries(patient_id):
    entries = db_handler.get_patient_mood_scores(patient_id)
    return jsonify(entries)


@app.route('/topic-sentiments/<string:patient_id>', methods=['GET'])
def get_patient_valence_entries(patient_id):
    entries = db_handler.get_patient_topics_sentiments(patient_id)
    result = parse_valence_entries(entries)
    return jsonify(result)


@app.route('/valence-datasets/<string:patient_id>', methods=['GET'])
def get_patient_valence_datasets(patient_id):
    """
    Fetch all legacy_wordcloud entries from DB to use in graph in FE to show sentiment over time per topic.
    """
    entries = db_handler.get_patient_topics_sentiments(patient_id)
    result = parse_valence_datasets(entries)
    return jsonify(result)


@app.route('/wordcloud/<string:patient_id>', methods=['GET'])
def get_patient_wordcloud(patient_id):
    wc_location = f'{config_instance.wc_location}/Patient_{patient_id}-wordcloud.png'
    with open(wc_location, 'rb') as f:
        image_data = f.read()
    return Response(image_data, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
