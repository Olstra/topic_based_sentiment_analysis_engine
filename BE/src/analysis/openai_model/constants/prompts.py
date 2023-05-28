SUMMARIZE = '''
Summarize this text in German. Maximum 280 characters:
'''
SUMMARIZE_TO_JSON = '''
I need the answer to my question as a JSON object. Do not give explanation.
Question: How would you rate this text with regards to the patients motivation. Measure motivation on a scala from 0-10. 
Write -1 if you cant find the needed information in the text.
Text: im Löwen gB es KEIN Vegi Menu!! muss ich strei hen an den Vegitagen. ich schaffe es nicht!!! zu spät nocj gegessen. am Morgen 1 lt Wasser bis 10:00
Answer: {"perceived_importance":-1,"chance_of_succ":1,"perceived_control":4,"meaningfulness":-1} 
Text:
'''
VALENCE = '''
I need the answer to my question as a JSON object. Do not give explanation. 
Question: What kind of topics do you identify in this text? List only topics that have to do with eating habits or 
sport activities. Check for synonyms and merge them within 1 topic. After detecting topics perform sentiment analysis on
them and write if the patient has a positive, negative or neutral sentiment with regards to that topic on a scala from -3 to 3. 
Text: Das Intervallfasten klappt ganz gut. Ich war am Montagabend schwimmen, und habe mich dabei nicht wohl gefühlt. 
Am Donnerstag ist mir etwas dazwischen gekommen und ich bin nicht ins Hallenbad. 
Answer: {"legacy_wordcloud":[{"topic":"Intervallfasten","sentiment":3},{"topic":"Schwimmen","sentiment":-2}]} 
Text:
'''
SENTIMENT_ANALYSIS = '''
Answer with number only. Calculate polarity score (-1 to 1) of this sentence:
Ich gehe Laufen 😎
0.9
Ich gehe
0.0
Ich gehe 😡
-0.9
'''
TOPIC_DETECTION = '''
I need the answer to my question as a python string. Do not give explanation. 
What are the topics of this sentence?:
input: "Ich gehe Schwimmen im Hallenbad."
output: Schwimmen
input:
'''