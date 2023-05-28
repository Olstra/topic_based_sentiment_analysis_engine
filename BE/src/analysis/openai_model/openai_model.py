import json
import logging
from dataclasses import asdict

import requests

import BE.src.analysis.openai_model.constants.prompts as prompts
from BE.src.analysis.openai_model.DTOs.ChatRequestDTO import ChatRequestDTO
from BE.src.analysis.openai_model.constants.api import URL
from BE.src.config import config_instance
from BE.src.preprocessing.emojis_parser import emojis_to_description

logging.basicConfig(level=logging.INFO)


class OpenaiModel:
    """
    Class for interacting with openai API.
    Define prompt through 'set_messages()'.
    Get Answer through 'answer_query()'
    """

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config_instance.chat_gpt_api_key}"
        }

        self.data = ChatRequestDTO(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'please set messages!'"}],
            temperature=0.2
        )

    def set_model(self, model_name):
        self.data.model = model_name

    def set_messages(self, prompt, new_role="user"):
        self.data.messages = [{"role": new_role, "content": prompt}]

    def set_temperature(self, temperature):
        self.data.temperature = temperature

    def get_prompt(self):
        return self.data.messages[0]["content"]

    def make_request(self):
        return requests.post(URL, headers=self.headers, data=json.dumps(asdict(self.data)))

    def answer_query(self):
        response = self.make_request()
        response_code = str(response.status_code)
        if response_code != '200':
            logging.error(f'Error while making request: {response_code}\nResponse: {response.json()}')
            return

        response_content = response.json()['choices'][0]['message']['content']

        logging.info(f'Successfully requested answer from API. Response was: {response_content}')

        return response_content

    def summarize_text_to_text(self, text: str, patient_gender: str):
        prompt = f'{prompts.SUMMARIZE}: {text}'
        self.set_messages(prompt)
        return self.answer_query()

    def summarize_text_to_json(self, text):
        prompt = f'{prompts.SUMMARIZE_TO_JSON}: {text}'
        self.set_messages(prompt)
        response = extract_json(self.answer_query())
        # response = add_average_motivation(response) # TODO: what if response was NONE
        return response

    def get_valence_activities(self, text) -> dict:
        prompt = f'{prompts.VALENCE}: {text}'
        self.set_messages(prompt)
        return extract_json(self.answer_query())

    def get_sentiment(self, text) -> float or None:
        prompt = f'{prompts.SENTIMENT_ANALYSIS}: {text}'
        self.set_messages(prompt)
        try:
            return float(self.answer_query())
        except (ValueError, TypeError) as e:
            logging.error(f"Error while parsing GPT's answer: {e}. Returning None...")
            return None

    def get_topics(self, text) -> str:
        text = emojis_to_description(text)
        prompt = f'{prompts.TOPIC_DETECTION}: {text}'
        self.set_messages(prompt)
        return self.answer_query()


def add_average_motivation(motivation_scores: dict):
    mood_avg = round((motivation_scores["perceived_importance"] + motivation_scores["chance_of_succ"] +
                      motivation_scores["perceived_control"] + motivation_scores["meaningfulness"]) / 4, 2)
    motivation_scores["overall_motivation"] = mood_avg
    return motivation_scores


def extract_json(input_txt: str) -> dict:
    """
    Sometimes chatGPT adds text to JSON answer. This function extracts only the JSON from answer.
    """
    sub_str = ""
    for c in input_txt[::-1]:
        if c == "}":
            break
        sub_str = c + sub_str
    # delete everything after the last '}'
    input_txt = input_txt.replace(sub_str, "")
    for c in input_txt:
        if c == "{":
            break
        sub_str = sub_str + c
    # delete everything before the first '{'
    input_txt = input_txt.replace(sub_str, "")
    # convert string to json object / dict
    json_obj = json.loads(input_txt)
    return json_obj


if __name__ == '__main__':
    model = OpenaiModel()
    example_text = "Im Moment ist mein Alltag eher eintönig, da mein Mann für Ausflüge zu wenig mobil ist. "
    answer = model.get_sentiment(example_text)
    print(answer)
