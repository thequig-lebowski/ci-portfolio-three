print('Would you like to play again?')
    replay = ['Yes', 'No']
    user_input = TerminalMenu(replay)
    input_index = user_input.show()
    action = replay[input_index]

    def difficulty_select():
    """
    Do stuff
    """
    diff_options = ['Easy', 'Medium', 'Hard']
    print('Please choose a difficulty level from the list below:\n')
    difficulty_menu = TerminalMenu(diff_options)
    diff_selection = difficulty_menu.show()
    rprint(f'You have selected [bold purple]{diff_options[diff_selection]}')
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
    rprint(f'You have selected [bold purple]{cat_options[cat_selection]}')
    return (cat_options[cat_selection], cat_selection)