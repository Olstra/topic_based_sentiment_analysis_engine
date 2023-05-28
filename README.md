# Topic detection and Sentiment Analysis Engine for use in Healthcare
### Description
As a project for my bachelor thesis I developed a sentiment analysis with topic detection engine. This engine is to be used in conjunction with the "Digital Companion" app to analyze patient adherence issues.<br>

Specifically, the engine will use chat histories with the patient to identify the reasons why they could not adhere to the therapy prescribed by the doctor. This information will be used to find solutions to these adherence problems.<br>

__Involved Persons__<br>
Student and developer: Oliver Strassmann<br>
Scientific assistant: Dr. Mateusz Dolata<br>
Assistant from Digital Companion project: Prof. Dr. Alexandre de Spindler<br>
Professor in charge: Prof. Dr. Gerhard Schwabe<br>

## Project setup
The project is structured like the follow:
- FE: Frontend - visualization of the performed analysis for the user
- BE: Backend application + API
- DB: contains database prefilled with exemplary data
- Data: contains the raw data used as example in this project

#### Setup backend
Install the needed python packages through _BE > requirements.txt_
#### Setup frontend
1. Install JS
2. Install Vue
3. Run:
```
$ cd FE
$ npm install
```
#### Optional: Setup .env file
If you want to feed custom data to the application, you will need to generate a .env file.<br>
You can do so by following the steps bellow.
1. Generate .env file by running:
```
$ cp BE/.env.example BE/.env
```
2. Add your valid ChatGPT API Key under CHAT_GPT_API_KEY
3. Change the other values if you want to provide custom test data or database

## Run application
1. Start API by running the file _BE>src>main.py_
2. Start frontend
```
$ cd FE
$ npm run dev
```
3. Open http://localhost:5173 on a webbrowser with CORS disabled.<br>
For example by running this command (macOS, Chrome):
```
$ open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security
```

## Use cases
- Lade eine vorhandene Konversation aus "/conversation_data_raw" um zu testen oder füge deine eigene hinzu.
Du kannst eine Konversation für die Analyse selektieren, indem du den Pfad zum File unter im .env File angibst.

## Testing

## Used Technologies
- Openai API
- JavaScript, TypeScript
- Vue
- Google JS Charts
- Python
- SQLite

## Licence
TBD
