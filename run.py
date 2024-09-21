import json
import requests
from pprint import pprint
import creds
from html import unescape

# Global Variables
QUESTIONS = {}



def getQuestion(amount, category, difficulty):
    """
    Function to get a set of questions from the Trivia Questions API.
    It stores the the list of 10 Q's in a variable to be called later
    """
    url = f"https://trivia-questions-api.p.rapidapi.com/triviaApi?amount={amount}&category={category}&difficulty={difficulty}"

    headers = {
        "x-rapidapi-key": creds.api_key,
        "x-rapidapi-host": "trivia-questions-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    # convert response object to python dict
    QUESTIONS = response.json()
    pprint(QUESTIONS, depth=5)
    print('\n')
    print('\n')
    i = 1
    this_question = QUESTIONS['triviaQuestions'][i]['question']
    # print(unescape(QUESTIONS['triviaQuestions'][0]['question']))
    print(unescape(this_question))
    correct_answer = QUESTIONS['triviaQuestions'][i]['correct_answer']
    print(unescape(f'The correct answer is: {correct_answer}'))

getQuestion(2, 9, 'easy')