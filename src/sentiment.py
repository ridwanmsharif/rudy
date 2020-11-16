import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions

BASE_URL = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com"

class Sentiment:
    def __init__(self, file):
        with open(file) as f:
          data = json.load(f)
          self.key = data['apikey']
          self.url = data["url"]

        authenticator = IAMAuthenticator(self.key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2020-08-01',
            authenticator=authenticator)

        natural_language_understanding.set_service_url(self.url)
        self.analyzer = natural_language_understanding
        return

    def analyze(self, text):
        if text == "empty" or text  == "":
            return 5.0

        response = self.analyzer.analyze(
            text=text,
            language='en',
            features=Features(sentiment=SentimentOptions(document=True))).get_result()
        return (float(response["sentiment"]["document"]["score"]) + 1) * 5

# s = Sentiment("apikey.json")
# res = s.analyze("")
# print(res)
