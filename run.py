import json
import requests
from pprint import pprint
import creds
from html import unescape
import random
import textwrap
from rich import print
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

    url = f"""https://trivia-questions-api.p.rapidapi.com/triviaApi?
    amount={amount}&category={category}&difficulty={difficulty}"""

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
        print(f'Qusetion {x+1}: ')
        print(unescape(this_question), '\n')

        incorrect_answers = question['incorrect_answers']
        correct_answer = question['correct_answer']
        answers = incorrect_answers + [correct_answer]
        print(f'cheat ans is: {correct_answer}')

        # shuffle answers if more than two options
        # otherwise sort into reverse alphabetical order
        # so that the True/False order is consistent
        if len(answers) > 2:
            random.shuffle(answers)
        else:
            answers.sort(reverse=True)

        display_answer_options(answers)

        while True:
            user_answer = input('Your answer: \n')
            if validate_answer(user_answer, x):
                check_answer(user_answer, correct_answer, answers)
                break

        x += 1
    game_over()


def display_answer_options(answers):
    """
    Print answers with numbered indexing.
    """
    answer_number = 1
    for answer in answers:
        # remove unwanted spaces
        answer.strip()
        print(unescape(f'No.{answer_number} {answer}'))
        answer_number += 1
    print('\n')


def check_answer(input_ans, correct_ans, ans_list):
    input_ans = int(input_ans)
    global SCORE
    ans_index = ans_list.index(correct_ans) + 1
    if input_ans == ans_index:
        print('Correct!\n')
        SCORE += 1
    else:
        print("Sorry, that's not right\n")


def game_over():
    """
    Function to display score and further options;
    play again view leader board.
    """
    # Use match/case statement to have dynamic congrats message
    # depending on the amount scored.
    global SCORE
    match SCORE:
        case 0:
            print('You didn\'t manage to get any questions right.')
        case SCORE if SCORE < 3:
            print(f'Not bad, you got {SCORE} right answers.')
        case SCORE if SCORE < 6:
            print(f'Well done, you were able to get {SCORE} questions right.')
        case SCORE if SCORE < 9:
            print(f'Great job, you scored {SCORE} out of 10.')
        case SCORE if SCORE < 10:
            print(textwrap.dedent(f'''You got {SCORE} questions
             right, nearly a perfect score. Well done!'''))
        case 10:
            print(textwrap.dedent('''CONGRATULATIONS! You scored
            a perfect round of 10/10. Well done.'''))
    # check leader board
    print('game over\n')


def validate_answer(ans, index):
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


def start_up():
    """
    Welcome screen, rules, set game category
    set game difficulty.
    """
    print('\n')
    print('Welcome to "LET\'S GET QUIZICAL"\n')
    print(textwrap.dedent('''
    This is a text-based quuiz game where you can 
    test your knowledge across several different categories 
    in either \'easy\', \'medium\' or \'hard\' mode.'''))


def validate_input(category, difficulty):
    """
    Validate user selection of category and difficulty level
    """
    pass


def main():
    """
    List of functions to run on programme launch
    """
    start_up()
    get_questions(10, 9, DIFFICULTY)
    display_questions()


main()