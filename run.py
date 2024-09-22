import json
import requests
from pprint import pprint
import creds
from html import unescape
import random
# import sample_data

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
    x = 0
    for question in QUESTIONS:
        this_question = question['question'] 
        print(unescape(this_question), '\n')
        incorrect_answers = question['incorrect_answers']
        correct_answer = question['correct_answer']
        # print('correct answer is type: ', type(correct_answer), correct_answer)
        # print('incorrect answers is type: ',type(incorrect_answers), incorrect_answers, '\n')
        answers = incorrect_answers + [correct_answer]
        
        # shuffle answers if more than two options
        # otherwise sort into reverse alphabetical order
        # so that the True/False order is consistent
        if len(answers) > 2:
            random.shuffle(answers)
        else:
            answers.sort(reverse = True)

        # print answers with number indexing
        answer_number = 1
        for answer in answers:
            # remove unwanted spaces
            answer.strip()
            print(unescape(f'No.{answer_number} {answer}'))
            answer_number += 1
        print('\n')
        while True:
            user_answer = input('Your answer: \n')
            if validate_input(user_answer, x):
                check_answer(user_answer, correct_answer, answers)
                break

        x += 1
    print('game over\n')

def check_answer(input_ans, correct_ans, ans_list):
    input_ans = int(input_ans)
    print('checking answer...\n')
    print(f'input_ans {type(input_ans)}')
    print(f'correc_ans {correct_ans}')
    print(f'ans_list {ans_list}')
    global SCORE
    ans_index = ans_list.index(correct_ans) + 1
    print(f'ans_index {ans_index}')
    if input_ans == ans_index:
        print('Correct!\n')
        SCORE += 1
    else:
        print("Sorry, that's not right\n")





def validate_input(ans, index):
    """
    Validate user input to be a number 1-4 or
    1-2 if answer is boolean.
    """
    ans_type = QUESTIONS[index]['type']
    ans_range = 4
    if ans_type == 'multiple':
        pass
    else:
        ans_range = 2
    
    try:
        ans = int(ans)
        if not (1 <= ans <= ans_range):
            raise ValueError(
                f"Expected an input of '1 - {ans_range}', but got '{ans}'."
            )    
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False


    return True


get_questions(3, 9, DIFFICULTY)
display_questions()