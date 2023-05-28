"""
The configuration for the application
"""
import os
from dotenv import load_dotenv

project_root = "BE"


def get_config_info():
    """
    Gets the Config File path
    :return: The Path to the current config file
    """
    while True:
        if project_root in os.listdir():
            break
        os.chdir('..')
    load_dotenv()
    return {
        'chatgpt-api-key': os.getenv('CHAT_GPT_API_KEY'),
        'deepl-api-key': os.getenv('DEEPL_API_KEY'),
        'raw-data-path': os.getenv('RAW_DATA_PATH'),
        'db-location': os.getenv('DB_LOCATION')
    }


class Config:
    """
    Holds all configuration Information needed for the application.
    Singleton.
    """

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

        # initialize attributes
        data = get_config_info()
        self.chat_gpt_api_key = str(data['chatgpt-api-key'])
        self.deepl_api_key = str(data['deepl-api-key'])
        self.raw_data_path = os.path.join(os.getcwd(), str(data['raw-data-path']))
        self.db_location = os.path.join(os.getcwd(), str(data['db-location']))

    def reload(self):
        """
        Reloads the config from the Environment
        :return: A instance of the Config
        """
        self.__init__()
        return self


# create unique instance of config
config_instance = Config()
