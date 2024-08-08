import sys
from pathlib import Path

from User import validate_login_details as validate_user
from User import update_user as update_user_info_to_system
from User import create_new_user
from Validation import validate_menu_choices
from Validation import validate_new_username
from Validation import validate_new_password
from Validation import validate_student_id
from Validation import validate_assignment_id
from Validation import validate_grade
from Submission import upload_assignment_to_system
from Submission import retrieve_specific_submission
from Submission import print_submission_contents
from Submission import initiate_submission_information
from Submission import store_submission_cache
from Submission import store_grade_to_file
from Submission import load_grades_from_json
from Submission import print_all_current_submissions
from Submission import calculate_average_score
from Submission import retrieve_highest_score_student
from Submission import display_student_not_meeting_threshold
from Submission import delete_file_from_data


def start_program():

    """
    This function acts as the starting point of the program, where the system will prompt the user to
    input their username and password.
    :return: None
    """

    # Initiate the necessary functions
    initiate_submission_information()

    # Introductory interface
    print("------------------------------------------------------------------")
    print("             Welcome to APU article management system!            ")
    print("------------------------------------------------------------------")

    # Prompt users to input login credentials
    display_interface_to_input_login_credentials()


def display_interface_to_input_login_credentials():

    """
    This function prompts user to input their username and password, then displays the menu if login is successful.
    :return: None
    """

    # Prompt users to input username and password
    prompted_username = input("Enter your username: ").lower().strip()
    prompted_password = input("Enter your password: ").strip()

    # Validate inputted username and password
    is_account_exist, user_object = validate_user(prompted_username, prompted_password)

    # Exit system if the account does not exist
    if not is_account_exist:
        print("\nInvalid credentials. The system will exit automatically.")
        sys.exit()

    # Welcome user and display menu if the account exists
    print("\nLogin successful! Welcome back, " + prompted_username + "!\n")
    display_menu(user_object)


def display_menu(user):

    """
    This function displays the menu options and allows users to input their choices
    :return: None
    """

    while True:
        # Menu interface
        print("------------------------------------------------------------------")
        print("                               Menu                               ")
        print("------------------------------------------------------------------")
        print("1.  Help")
        print("2.  Add a user")
        print("3.  Exit")
        print("4.  Add a submission from student")
        print("5.  Grade a student's submission")
        print("6.  List all submissions")
        print("7.  List all submissions that have not been graded")
        print("8.  Display the average score")
        print("9.  Display the student who has the highest score")
        print("10. Display students whose score is less than a threshold")
        print("11. Store the grade to a JSON file")
        print("12. Load the grade from a JSON file")
        print("13. Delete a submission and its grade")
        print("14. Modify username and password")
        print("------------------------------------------------------------------")

        # Prompt for choice
        choice = input("Please provide your choice: ")

        # Validate menu choices
        is_input_valid = validate_menu_choices(choice)

        # Prompt user to input again if input is invalid
        if not is_input_valid:
            print("\nInvalid choice. Please provide a valid choice.\n")
            continue

        # Proceed to the corresponding interfaces if input is valid
        if choice == "1":

            # Displays the menu again
            print("\nKey in a number that corresponds to the action you wish to perform.\n")

        elif choice == "2":

            # Run function to add new user
            add_new_user()

        elif choice == "3":

            # Check if user wishes to exit the program
            is_exit = exit_program()

            # Exit the program if yes
            if is_exit:
                sys.exit()

            # Blank space to make display organized
            print("")

        elif choice == "4":

            # Run function to add submission to the system
            add_file_to_system()

        elif choice == "5":

            # Run function to grade a submission
            grade_submission()

        elif choice == "6":

            # Run function to print out all submissions
            print_all_submissions()

        elif choice == "7":

            # Run function to print graded submissions
            print_all_submissions(filter_condition=1)

        elif choice == "8":

            # Run function to print average score
            display_average_score()

        elif choice == "9":

            # Run function to print students with the highest score for each assignment
            display_student_with_highest_score()

        elif choice == "10":

            # Run function that filters students with a minimum threshold
            display_student_with_threshold()

        elif choice == "11":

            # Run function to store the grades of the current Submission objects to JSON file
            store_current_grade_to_json()

        elif choice == "12":

            # Run function to retrieve grade from the external JSON file
            retrieve_grade_from_json()

        elif choice == "13":

            # Run function to delete submission file and grade
            delete_submission()

        elif choice == "14":

            # Prompt user to input their new username and password, then display the menu again once finished
            update_username_and_password(user)


def add_new_user():

    """
    This function prompts the user to create a new user by inputting a new username and password.
    :return: None
    """

    while True:
        # Prompt for new username
        new_username = input("\nEnter a new username: ").lower().strip()

        # Validate username
        is_username_valid = validate_new_username(new_username, is_modify_own=False)

        # Exit loop if username meets condition
        if is_username_valid:
            break

        # Continue loop if username does not fulfill criteria
        print("Your username is either being used, or does not have a length between 3 to 15 characters. "
              "Please try again.")

    while True:
        # Prompt for new password
        new_password = input("Enter a new password: ").strip()

        # Validate password
        is_password_valid = validate_new_password(new_password)

        # Exit loop if password meets condition
        if is_password_valid:
            break

        # Continue loop if password does not meet criteria
        print("Password has to be between 3 and 15 characters, and a combination of letters and numbers. "
              "Please try again.\n")

    # Create a new user object
    create_new_user(new_username, new_password)
    print("\nNew user has been created. You will be redirected to the main menu.\n")


def exit_program():

    """
    This function confirms that the user wishes to exit the program.
    :return: True if the user wishes to exit, False otherwise.
    """

    while True:
        # Prompt user for input
        exit_prompt = input("\nAre you sure you want to logout and exit the program (Y/N): ").lower().strip()

        # Request user to input again if input is invalid
        if exit_prompt in ["y", "n"]:
            break

        print("Invalid input. Please input a valid choice.")

    # Return true if user wishes to log out
    if exit_prompt == "y":
        print("\nThank you for using the system. The system will exit automatically.")
        return True

    # Return false if user inputs "n"
    else:
        return False


def add_file_to_system():

    """
    This function prompts a file path from user to copy a file to the system.
    :return: None
    """

    while True:
        # Prompt for student ID
        student_id = input("\nPlease enter the student id: ").upper().strip()

        # Validate student_id
        is_id_valid = validate_student_id(student_id)

        # Exit loop if ID is appropriate
        if is_id_valid:
            break

        # Continue the loop if the format is incorrect
        print("Invalid format (ex: S068495). Please provide a proper student ID.")

    while True:
        # Prompt for assignment ID
        assignment_id = input("Please enter the assignment id: ").upper().strip()

        # Validate assignment ID
        is_assignment_valid = validate_assignment_id(assignment_id)

        # Exit loop if ID is correct
        if is_assignment_valid:
            break

        # Continue the loop if ID is invalid
        print("Invalid format (ex: A0012). Please provide a proper assignment ID.\n")

    # Prompt for the text file path
    file_path = input("Please enter the assignment file path: ").strip()

    # Attempt to copy the file from file_path to destination
    upload_successful = upload_assignment_to_system(file_path, student_id, assignment_id)

    # Prompt message if upload is successful or unsuccessful
    if upload_successful:
        print("\nUpload successful. You will be redirected to the main menu.")
        print("Note: You will need to run Option 11 to reflect the grades of the file into the JSON file.\n")
    else:
        print("\nUpload unsuccessful. You will be redirected to the main menu, please try again.\n")


def grade_submission():

    """
    This function allows users to provide a grade to each assignment.
    :return: None
    """

    # Prompt for student ID and assignment ID
    student_id = input("\nPlease enter the student ID: ").upper().strip()
    assignment_id = input("Please enter the assignment ID: ").upper().strip()

    # Retrieve the full list of submissions
    submission_list = initiate_submission_information()

    # Search for the relevant submission object
    submission = retrieve_specific_submission(student_id, assignment_id, submission_list)

    # Return to the menu if submission is not found
    if not submission:
        print("\nThe submission you entered does not exist. You will be redirected to the main menu.")
        print("Please try again.\n")
        return None

    # If the submission has already been graded before
    if submission.grade != "/":
        print("\nThe submission has already been graded. Providing a new mark will overwrite its existing grade.")
        print("Note: The existing mark is: " + submission.grade)

        while True:
            # Ask user if they wish to proceed with modification
            is_proceed = input("Do you wish to continue (Y/N): ").lower().strip()

            # Ask user to provide a proper input
            if is_proceed not in ["y", "n"]:
                print("Please provide a valid choice.\n")
                continue

            # Return to the main menu if the user does not wish to proceed
            if is_proceed == "n":
                print("You will be redirected to the main menu.")
                return None

            # Exit loop if the user wishes to proceed with modification
            break

    # Print the contents from the corresponding submission file
    print("\n------------------------------------------------------------------")
    print("The contents of the submission are:")
    print("------------------------------------------------------------------")
    print_submission_contents(submission)
    print("------------------------------------------------------------------")

    while True:
        # Prompt for grade
        new_grade = input("Provide a grade for the submission: ")

        # Validate the new_grade
        is_valid = validate_grade(new_grade)

        # Continue the loop if grade is not valid
        if not is_valid:
            print("Please provide a valid grade (0 - 100). Try again.\n")
            continue

        # Exit the loop if the new grade is valid
        break

    # Store the new grade to the Submission object
    submission.grade = new_grade

    # Store the submission list as a cache
    store_submission_cache(submission_list)

    # Remind user that the grade is not stored into the JSON file
    print("\nMarks have been updated. Note that the marks are not saved into the JSON file yet.")
    print("Run Option 11 to store the marks to the JSON file.")
    print("\nYou will be redirected to the main menu.\n")


def print_all_submissions(filter_condition=0):

    """
    This function aims to print out the information of all submissions.
    :param filter_condition: '1' to print ungraded, else None for all submissions.
    :return: None
    """

    # Introductory prompt
    print("\nBelow are the list of submissions:")

    # Run function to print information
    print_all_current_submissions(filter_condition)

    # Empty line to make things organized
    print("")


def display_average_score():

    """
    This function displays the average score of an assignment, or all submissions if input is ALL.
    :return: None
    """

    # Prompt for assignment ID
    assignment_id = input("\nPlease enter the assignment ID ('ALL' for overall average): ").upper().strip()

    # Run function to retrieve the average score
    average_score = calculate_average_score(assignment_id)

    # Inform users that the assignment ID is invalid
    if average_score == -1:
        print("\nInvalid assignment ID. Please try again.")

    # Display marks if assignment ID is valid
    else:
        print("\nThe average score is: " + str(average_score) + "\n")

    # Inform users that they will be redirected back to the main menu
    print("You will be redirected back to the main menu.\n")


def display_student_with_highest_score():

    """
    This function displays the student with the highest score for each assignment.
    :return: None
    """

    # Introductory line
    print("\nBelow are the students who scored the best for each assignment:")

    # Run function to print submission information
    retrieve_highest_score_student()

    # Empty line to make things organized
    print("")


def display_student_with_threshold():

    """
    This function aims to display the student who does not meet a specific mark for a specific assignment.
    :return: None
    """

    # Prompt user to input assignment ID and threshold
    assignment_id = input("\nPlease enter the assignment ID: ").upper().strip()
    threshold = input("Please enter the mark threshold: ").strip()

    # Validate assignment_id
    is_assignment_valid = validate_assignment_id(assignment_id)
    if not is_assignment_valid:
        print("\nInvalid assignment ID. Please try again from the main menu.\n")
        return None

    # Validate threshold inputted
    is_threshold_valid = validate_grade(threshold)

    # Return to the main menu if the threshold is invalid
    if not is_threshold_valid:
        print("\nPlease provide a valid threshold (0 - 100). Try again from the main menu.\n")
        return None

    # Run function to retrieve the students
    display_student_not_meeting_threshold(assignment_id, threshold)


def store_current_grade_to_json():

    """
    This function aims to store the cached grades into the JSON file.
    :return: None
    """

    # Load function to upload grades to JSON.
    store_grade_to_file()

    # Notify users that the grades have already been updated.
    print("\nThe grades are saved to the JSON file.")
    print("You will be redirected to the main menu.\n")


def retrieve_grade_from_json():

    """
    This function aims to retrieve the grades from the JSON file to the system.
    :return: None
    """

    # Prompt path to the external JSON file
    external_path = input("\nPlease provide the path to the external JSON file: ").strip()

    # Return to the main menu if the path is invalid
    is_path_exist = Path(external_path).exists()
    if not is_path_exist or external_path == "":
        print("\nThe path does not exist. You will be redirected to the main menu.\n")
        return None

    # Run function to load grades from JSON
    is_load_to_json = load_grades_from_json(external_path)

    # Validate if users do not want to put data in JSON
    if not is_load_to_json:
        print("\nThe grades were not loaded. Please run Option 11 to store the grades to the system.")
        print("You will be redirected to the main menu.\n")

    # Notify user about the retrieval of grades
    else:
        print("\nThe grades are retrieved from the JSON file.")
        print("Run Option 6 to view the grades of all assignments.\n")


def delete_submission():

    """
    This function aims to delete the submission text file and the corresponding grade.
    :return: None
    """

    # Prompt for assignment ID and student ID
    assignment_id = input("\nPlease enter the assignment ID: ").upper().strip()
    student_id = input("Please enter the student ID: ").upper().strip()

    # Validate assignment_id
    is_assignment_valid = validate_assignment_id(assignment_id)
    if not is_assignment_valid:
        print("\nInvalid assignment ID.")

    # Run function to search for the corresponding file and delete the grade
    is_deleted = delete_file_from_data(assignment_id, student_id)

    # Inform the user that the file is deleted if the file exists
    if is_deleted:
        print("\nThe submission file and the corresponding grade is deleted.")
        print("You will be redirected to the main menu.\n")
        return None

    # Ask user to try again if the file is not found
    print("\nThe associated file is not found. Please try again.")
    print("You will be redirected to the main menu.\n")
    return None


def update_username_and_password(user):

    """
    This function allows users to modify the existing username and password.
    :param user: The user to modify
    :return: None
    """

    while True:
        # Prompt user to input a new username
        new_username = input("\nPlease enter your new username: ").lower().strip()

        # Validate username
        if not validate_new_username(new_username, is_modify_own=True, user_object=user):
            print("Invalid username. Please insert a username with length between 3 and 15.")
            continue

        # Exit loop if username matches condition
        break

    while True:
        # Prompt user to input a new password
        new_password = input("Please enter your new password: ").strip()

        # Validate password and exit loop if password matches condition
        if validate_new_password(new_password):
            break

        # Continue loop if password is invalid
        print("Invalid password. Please insert a password with length between 3 and 15, "
              "with combination of letters and numbers.\n")

    # Modify new username and password
    user.username = new_username
    user.password = new_password

    # Store modification to file
    update_user_info_to_system(user)
    print("\nUser information is saved. You will be redirected to the main menu.\n")
