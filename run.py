import json
import requests
from pprint import pprint
import creds
from html import unescape
import random

# Global Variables
QUESTIONS = []
USERNAME = ''
SCORE = 0
DIFFICULTY = 'easy'



def get_questions(amount, category, difficulty):
    """
    Function to get a set of questions from the Trivia Questions API.
    It stores the the list of 10 Q's in a variable to be called later
    """
    print('fetching questions...\n')

    url = f"https://trivia-questions-api.p.rapidapi.com/triviaApi?amount={amount}&category={category}&difficulty={difficulty}"

    headers = {
        "x-rapidapi-key": creds.api_key,
        "x-rapidapi-host": "trivia-questions-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    # convert response object to python dict
    global QUESTIONS
    QUESTIONS = response.json()
    QUESTIONS = QUESTIONS['triviaQuestions']
    # print('QUESTIONS type is:', type(QUESTIONS))
    # print('QUESTIONS length is:', len(QUESTIONS))


    # pprint(QUESTIONS, depth=5)
    i = 1
    this_question = QUESTIONS[i]['question']
    correct_answer = QUESTIONS[i]['correct_answer']
    incorrect_answers_list = QUESTIONS[i]['incorrect_answers']
    
    # print('number of questions: ', len(QUESTIONS))
    # print(unescape(this_question))
    # print(unescape(f'The correct answer is: {correct_answer}'))
    # print(unescape(f'The wrong answers are: {incorrect_answers_list}'))
    # return a string with 1)The question 2)the correct answer and 3)the incorrect answers
    # return [this_question, correct_answer]


def display_questions():
    """
    Display the questions, one at a time with the multiply choice
    answers below and take the users answer to be checked
    """
    print('printing questions...\n')
    for question in QUESTIONS:
        this_question = question['question'] 
        print(unescape(this_question), '\n')
        incorrect_answers = question['incorrect_answers']
        correct_answer = question['correct_answer']
        # print('correct answer is type: ', type(correct_answer), correct_answer)
        # print('incorrect answers is type: ',type(incorrect_answers), incorrect_answers, '\n')
        answers = incorrect_answers + [correct_answer]
        random.shuffle(answers)
        # print answers with number indexing
        answer_number = 1
        for answer in answers:
            print(unescape(f'No.{answer_number} {answer}'))
            answer_number += 1
        print('\n')
        user_answer = input('Your answer: \n')
   




get_questions(2, 9, DIFFICULTY)
display_questions()