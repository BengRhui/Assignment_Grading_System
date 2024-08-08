from User import retrieve_user_information


def validate_menu_choices(inputted_choice):

    """
    This function aims to validate the choices entered by the user from the menu.
    :param inputted_choice:
    :return: True if choice is valid, else False
    """

    # Available options in menu
    available_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    try:
        # Check if input is blank
        if inputted_choice == "\n" or inputted_choice == "":
            raise ValueError

        # Check if input can be converted into an integer
        inputted_choice = int(inputted_choice)

        # Check if input is within the available options
        if inputted_choice not in available_options:
            raise ValueError

    # Return False if input does not satisfy condition
    except ValueError:
        return False

    # Return True if input is within 1 (inclusive) to 13 (inclusive)
    return True


def validate_new_username(inputted_username, is_modify_own, user_object=None):

    """
    This function aims to validate the new username entered by the user.
    :param inputted_username: Username inputted by the user.
    :param is_modify_own: Is the user modifying his own username?
    :param user_object: The user object if the user is modifying his own credentials.
    :return: True if username is valid, else False
    """

    # Return false if username does not have a length between 3 and 15
    if len(inputted_username) < 3 or len(inputted_username) > 15:
        return False

    # Return false if username is already taken
    user_list = retrieve_user_information()
    for user in user_list:

        # When adding a new user, check whether if the inputted username is already in the system
        if user.username == inputted_username and not is_modify_own:
            return False

        # When modifying own credentials, check whether if the inputted username is being taken, except if
        # the inputted username is the initial username
        elif is_modify_own and inputted_username != user_object.username and inputted_username == user.username:
            return False

    # Return true if username matches condition
    return True


def validate_new_password(inputted_password):

    """
    This function aims to validate the new password entered by the user.
    :param inputted_password:
    :return: True if password is valid, else False
    """

    # Counter to count the number of alphabets and numbers in the inputted password
    number_counter = 0
    alphabet_counter = 0

    # Return false if password does not have a length between 3 and 15
    if len(inputted_password) < 3 or len(inputted_password) > 15:
        return False

    # Count the number of numbers and alphabets in password
    for character in inputted_password:
        if character.isalpha():
            alphabet_counter += 1
        elif character.isdigit():
            number_counter += 1

    # Return false if password does not contain both number and alphabet
    if number_counter == 0 or alphabet_counter == 0:
        return False

    # Return true if password matches the conditions
    return True


def validate_student_id(student_id):

    """
    This function aims to validate the student id entered by the user.
    :param student_id: The student ID keyed-in by the user.
    :return: False if student id is invalid, else True
    """

    # Check if the total length is 7
    if len(student_id) != 7:
        return False

    # Check if student ID starts with S
    if student_id[0] != "S":
        return False

    # Return true if all conditions are met
    return True


def validate_assignment_id(assignment_id):

    """
    This function aims to validate the assignment id entered by the user.
    :param assignment_id: Assignment ID input by the user.
    :return: True if assignment ID is valid, else False
    """

    # Check if assignment ID has 5 characters in total
    if len(assignment_id) != 5:
        return False

    # Check if assignment ID starts with "A"
    if assignment_id[0] != "A":
        return False

    # Return true if all criteria are met
    return True


def validate_grade(grade):

    """
    This function aims to validate the grade entered by the user.
    :param grade: The inputted grade.
    :return: True if grade is valid, else False
    """

    try:
        # Convert the grade into an integer
        grade = int(grade)

        # Reject negative values and values greater than 100
        if grade < 0 or grade > 100:
            raise ValueError

    # Return false if the grade does not meet conditions
    except ValueError:
        return False

    # Return true if the grade is valid
    return True
