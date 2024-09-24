import json
import requests
from html import unescape
import random
import textwrap
from rich import print
import os
import time
from simple_term_menu import TerminalMenu
from dotenv import load_dotenv
import sys

# Global Variables
QUESTIONS = []
SCORE = 0
CATEGORY = 12
DIFFICULTY = 'hard'


# Functions
def configure():
    """
    Sets up .env for api keys
    """
    load_dotenv()


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
    print(f'Loading {amount} questions...\n')
    time.sleep(1)

    url = f"https://trivia-questions-api.p.rapidapi.com/triviaApi?amount={amount}&category={category}&difficulty={difficulty}"  # nopep8

    headers = {
        "x-rapidapi-key": os.getenv('api_key'),
        "x-rapidapi-host": "trivia-questions-api.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)

    # convert response object to python dict
    global QUESTIONS
    QUESTIONS = response.json()
    QUESTIONS = QUESTIONS['triviaQuestions']

    display_questions()


def display_questions():
    """
    Display the questions, one at a time with the multiply choice
    answers below and take the users answer to be checked
    """
    clr_terminal()
    x = 0
    for question in QUESTIONS:

        this_question = question['question']
        this_question = format_data(this_question)
        print(f'[bold bright_cyan]Qusetion {x+1}:[/bold bright_cyan]           [bold yellow1]Score {SCORE}/{x+1}\n')
        print(textwrap.fill(textwrap.dedent(this_question)), '\n')

        incorrect_answers = question['incorrect_answers']
        correct_answer = question['correct_answer']
        answers = incorrect_answers + [correct_answer]

        correct_answer = format_data(correct_answer)
        answers = format_data(answers)

        # shuffle answers if more than two options
        # otherwise sort into reverse alphabetical order
        # so that the True/False order is consistent
        if len(answers) > 2:
            random.shuffle(answers)
        else:
            answers.sort(reverse=True)

        time.sleep(1.5)
        user_answer = display_answer_options(answers)
        check_answer(user_answer, correct_answer)

        x += 1

    round_over()


def format_data(data):
    """
    Function to strip leading and trailing white space
    As well as unescaping special characters
    """
    if type(data) == str:
        data = unescape(data.strip())
        return data
    for x in data:
        new_x = unescape(x.strip())
        data[data.index(x)] = new_x
    return data


def display_answer_options(answers):
    """
    Print answers with numbered indexing.
    """
    answer_menu = TerminalMenu(answers)
    answer_selection = answer_menu.show()
    print(f'You have selected {answers[answer_selection]}\n')
    return answers[answer_selection]
    print('\n')


def check_answer(input_ans, correct_ans):
    """
    Function to compare selected ans with actual
    correct answer
    """
    global SCORE
    if input_ans == correct_ans:
        print('[bold green]Correct!\n')
        SCORE += 1
    else:
        print("[bold red]Sorry, that's not right\n")
    time.sleep(1.5)
    clr_terminal()


def round_over():
    """
    Function to display score and further options;
    play again view leader board.
    """
    global SCORE
    match SCORE:
        case 0:
            print('You didn\'t manage to get any questions right.')
        case SCORE if SCORE < 3:
            print(f'Not bad, you got [bold purple]{SCORE}[/bold purple] right answers.')
        case SCORE if SCORE < 6:
            print(f'Well done, you were able to get [bold purple]{SCORE}[/bold purple] questions right.')
        case SCORE if SCORE < 9:
            print(f'Great job, you scored [bold purple]{SCORE}[/bold purple] out of 10.')
        case SCORE if SCORE < 10:
            print(f'You got [bold purple]{SCORE}[/bold purple] questions right, nearly a perfect score. Well done!\n')
        case 10:
            print('CONGRATULATIONS! You scored a perfect round of [bold purple]10/10.[/bold purple] Well done.\n')

    time.sleep(4)
    clr_terminal()
    SCORE = 0
    replay_menu()


def replay_menu():
    """
    Asks the user what they would like to
    do when they get to the end of a round.
    """
    print('What would you like to do?\n')
    replay = [
        'Replay this round',
        'Try another category',
        'Exit'
        ]
    user_input = TerminalMenu(replay)
    input_index = user_input.show()
    action = replay[input_index]

    match action:
        case 'Replay this round':
            get_questions(10, CATEGORY, DIFFICULTY)
        case 'Try another category':
            main()
        case 'Exit':
            exit_programme()


def exit_programme():
    """
    Exits the programme safely
    """
    print('Exiting programme...')
    sys.exit(0)


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
    This is a text-based quiz game where you can
    test your knowledge across several different categories
    and difficulties.\n'''))
    time.sleep(1.5)
    print("Use the arrow keys to navigate, then press 'Enter' to select\n")
    (category, cat_index) = category_select()
    time.sleep(1.5)
    difficulty = difficulty_select()
    difficulty = difficulty.lower()
    time.sleep(1.5)
    category = convert_selection(cat_index)

    return (category, difficulty)


def difficulty_select():
    """
    Menu for the user to select the difficulty level
    for that round
    """
    diff_options = ['Easy', 'Medium', 'Hard']
    print('Please choose a difficulty level from the list below:\n')
    difficulty_menu = TerminalMenu(diff_options)
    diff_selection = difficulty_menu.show()
    print(f'You have selected [bold purple]{diff_options[diff_selection]}\n')
    return diff_options[diff_selection]


def category_select():
    """
    Menu for the user to select the category for that level
    """
    cat_options = [
        'General Knowledge',
        'Literature',
        'Film',
        'Music',
        'Television',
        'Sports',
        'Geography',
        'History'
    ]
    print('Please choose a category of questions from the list below:\n')
    category_menu = TerminalMenu(cat_options)
    cat_selection = category_menu.show()
    print(f'You have selected [bold purple]{cat_options[cat_selection]}\n')
    return (cat_options[cat_selection], cat_selection)


def convert_selection(selection):
    """
    Convert menu indices into API readable values
    """
    api_categories = [9, 10, 11, 12, 14, 21, 22, 23]
    return api_categories[selection]


def main():
    """
    List of functions to run on programme launch
    """
    configure()
    global CATEGORY
    global DIFFICULTY
    (CATEGORY, DIFFICULTY) = start_up()
    get_questions(10, CATEGORY, DIFFICULTY)


main()
