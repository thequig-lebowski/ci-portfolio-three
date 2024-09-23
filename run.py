import json
import requests
from pprint import pprint
import creds
from html import unescape
import random
import textwrap
from rich import print as rprint
import os
import time
from simple_term_menu import TerminalMenu

# import sample_data

# Global Variables
QUESTIONS = []
USERNAME = ''
SCORE = 0
DIFFICULTY = 'easy'


def clr_terminal():
    """
    Function to clear text from terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_questions(amount, category, difficulty):
    """
    Function to get a set of questions from the Trivia Questions API.
    It stores the the list of 10 Q's in a variable to be called later
    """
    print('Loading questions...\n')

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
    clr_terminal()
    # print('printing questions...\n')
    x = 0
    for question in QUESTIONS:

        this_question = question['question']
        rprint(f'[bold bright_cyan]Qusetion {x+1}: ')
        print(textwrap.dedent(unescape(this_question)), '\n')

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

        time.sleep(1.5)
        display_answer_options(answers)
        TEMPANSWER = answers.index(correct_answer) + 1 #delete this

        while True:
            # user_answer = input('Your answer: \n')
            user_answer = TEMPANSWER # delete this
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
        answer = answer.strip()
        print(unescape(f'No.{answer_number} {answer}'))
        answer_number += 1
        time.sleep(.2)
    print('\n')


def check_answer(input_ans, correct_ans, ans_list):
    input_ans = int(input_ans)
    global SCORE
    ans_index = ans_list.index(correct_ans) + 1
    if input_ans == ans_index:
        rprint('[bold green]Correct!\n')
        SCORE += 1
    else:
        rprint("[bold red]Sorry, that's not right\n")
    time.sleep(1.5)
    clr_terminal()


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
            rprint('You didn\'t manage to get any questions right.')
        case SCORE if SCORE < 3:
            rprint(f'Not bad, you got [bold purple]{SCORE}[/bold purple] right answers.')
        case SCORE if SCORE < 6:
            rprint(f'Well done, you were able to get [bold purple]{SCORE}[/bold purple] questions right.')
        case SCORE if SCORE < 9:
            rprint(f'Great job, you scored [bold purple]{SCORE}[/bold purple] out of 10.')
        case SCORE if SCORE < 10:
            rprint(textwrap.dedent(f'''
            You got [bold purple]{SCORE}[/bold purple] questions
             right, nearly a perfect score. Well done!'''))
        case 10:
            rprint(textwrap.dedent('''
            CONGRATULATIONS! You scored a perfect round
            of [bold purple]10/10.[/bold purple]Well done.'''))
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
    rprint('Welcome to "LET\'S GET QUIZICAL"\n')
    rprint(textwrap.dedent('''
    This is a text-based quuiz game where you can 
    test your knowledge across several different categories 
    and difficulties.\n'''))
    time.sleep(1.5)
    (category, cat_index) = category_select()
    rprint(f'You have selected [bold purple]{category}.')
    time.sleep(1.5)
    difficulty = difficulty_select()
    rprint(f'You have selected [bold purple]{difficulty}.')
    time.sleep(1.5)
    category = convert_selection(cat_index)

    return (category, difficulty)


def difficulty_select():
    """
    Do stuff
    """
    diff_options = ['easy', 'medium', 'hard']
    print('Please choose a difficulty level from the list below:\n')
    difficulty_menu = TerminalMenu(diff_options)
    diff_selection = difficulty_menu.show()
    return diff_options[diff_selection]


def category_select():
    """
    Do stuff
    """
    cat_options = [
        'General Knowledge', 'Literature', 'Film', 'Music', 
        'Television', 'Sports', 'Geography', 'History' 
    ]
    print('Please choose a category of questions from the list below:\n')
    category_menu = TerminalMenu(cat_options)
    cat_selection = category_menu.show()
    # print(f'You have selected {cat_options[menu_selection]}')
    return (cat_options[cat_selection], cat_selection)


def convert_selection(selection):
    """
    Do stuff
    """
    api_categories = [9, 10, 11, 12, 14, 21, 22, 23]
    return api_categories[selection]




def validate_input(category, difficulty):
    """
    Validate user selection of category and difficulty level
    """
    pass


def main():
    """
    List of functions to run on programme launch
    """
    (a, b) = start_up()
    get_questions(10, a, b)
    display_questions()


main()