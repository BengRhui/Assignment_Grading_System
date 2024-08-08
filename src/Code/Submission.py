import json
import os
import shutil
from pathlib import Path
from Data_IO import retrieve_submission_grade_from_file
from Data_IO import load_grades_into_json
from Data_IO import remove_submission_file
from Data_IO import sort_submission_array


class Submission:

    # The list acts as a cache to store temporary submission data
    SUBMISSION_LIST = []

    def __init__(self, student_id, assignment_id, grade="/"):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.grade = grade

    def __str__(self):
        return "Assignment ID: " + self.assignment_id + ", Student ID: " + self.student_id + ", Score: " + self.grade


def initiate_submission_information():

    """
    This function aims to set up the information of the submissions by retrieving the names of each submission
    and add grades to each corresponding submission based on contents in JSON file.
    :return: Array with Submission objects
    """

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    data_folder_directory = os.path.join(parent_directory, "Data")

    # Empty array to store submission objects
    submission_list = []

    # Create submission objects
    for file in os.listdir(data_folder_directory):

        # Continue loop if the file does not end with ".txt"
        if not file.endswith(".txt"):
            continue

        # Remove the .txt suffix first
        file_name = os.path.splitext(file)[0]

        # Separate text file names to retrieve student ID and assignment ID
        file_name = file_name.split("_")
        student_id = file_name[0]
        assignment_id = file_name[1]

        # Retrieve the stored corresponding grade for the assignment
        assignment_grade = retrieve_submission_grade_from_file(student_id, assignment_id)

        # Now we can create the submission object
        submission = Submission(student_id, assignment_id, assignment_grade)
        submission_list.append(submission)

    # Arrange the list
    submission_list = sort_submission_array(submission_list)

    # Store the list into cache
    for submission in submission_list:
        Submission.SUBMISSION_LIST.append(submission)

    # Return list containing all submission objects
    return submission_list


def upload_assignment_to_system(source_file_path, student_id, assignment_id):

    """
    This function aims to copy the text file from the path and place it under the Data folder.
    :param source_file_path: The initial file path of the submission / assignment.
    :param student_id: Student ID of the submitted assignment.
    :param assignment_id: Assignment code for the submission.
    :return: False if the file path does not exist, True if the file is successfully relocated.
    """

    # Check if the file path exists
    is_path_exist = Path(source_file_path).exists()
    if not is_path_exist or source_file_path == "":
        return False

    # Navigate to the Data folder
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    destination_folder = os.path.join(parent_directory, "Data")

    # Create name for the new file
    new_file_name = student_id + "_" + assignment_id + ".txt"
    destination_path = os.path.join(destination_folder, new_file_name)

    # Copy file to destination
    os.makedirs(destination_folder, exist_ok=True)
    shutil.copy(source_file_path, destination_path)

    # Create a new Submission object
    new_submission = Submission(student_id, assignment_id)

    # Add the new file to the cache array so that the cache is always updated
    Submission.SUBMISSION_LIST.append(new_submission)

    return True


def retrieve_specific_submission(student_id, assignment_id, submission_list):

    """
    This function aims to retrieve a specific submission based on student ID and assignment ID.
    :param student_id: The student ID of the submitted assignment.
    :param assignment_id: The ID of the assignment.
    :param submission_list: The submission list that contains all submissions.
    :return: A Submission object.
    """

    # Loop through the list to find the corresponding submission
    for submission in submission_list:

        # If the student ID does not match or the assignment ID does not match, continue the loop
        if submission.student_id != student_id or submission.assignment_id != assignment_id:
            continue

        # Retrieve the submission object if both the student ID and assignment ID match
        return submission

    # Return None if no Submission object matches the criteria
    return None


def print_submission_contents(submission_object):

    """
    This function aims to print the contents of the submission file.
    :param submission_object: The Submission object associated.
    :return: None
    """

    # Form the file name
    file_name = submission_object.student_id + "_" + submission_object.assignment_id + ".txt"

    # Navigate to the Data folder
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    destination_folder = os.path.join(parent_directory, "Data")

    # Retrieve the corresponding destination path
    destination_path = os.path.join(destination_folder, file_name)

    # Print contents from the path
    submission_contents = open(destination_path, 'r')
    for line in submission_contents.readlines():
        print(line)


def store_submission_cache(submission_list):

    """
    This function aims to store the submission list as a cache so that the information can be retrieved later.
    :param submission_list: The temporary list of submission objects.
    :return: None
    """

    # Clear the SUBMISSION_LIST array
    Submission.SUBMISSION_LIST.clear()

    # Update the SUBMISSION_LIST array
    for submission in submission_list:
        Submission.SUBMISSION_LIST.append(submission)


def store_grade_to_file():

    """
    This function aims to transform the SUBMISSION_LIST array into dictionary before storing it into the JSON file.
    :return: None
    """

    # Empty variable to hold data
    data = {}

    # Transform SUBMISSION_LIST into dictionary
    for submission in Submission.SUBMISSION_LIST:

        # Convert from Submission object to dictionary
        individual_data = {
            submission.assignment_id: {
                submission.student_id: submission.grade
            }
        }

        # Update the data dictionary
        data.update(individual_data)

    # Run function to write the dictionary into the JSON file
    load_grades_into_json(data)


def load_grades_from_json(path):

    """
    This function aims to load grades from an external JSON file into the SUBMISSION_LIST cache.
    :param path: Path for the external JSON file.
    :return: None
    """

    # Retrieve data from the JSON file
    contents = json.load(open(path, 'r'))

    # Empty array to record whether the Submission object from SUBMISSION_LIST is modified
    is_modified = False

    # Loop through each submission
    for submission in Submission.SUBMISSION_LIST:

        # Try to find the corresponding assignment ID
        for assignment_id, student_with_grade in contents.items():

            # Continue loop if assignment ID does not match
            if assignment_id != submission.assignment_id:
                continue

            # Find for the corresponding student ID
            for student_id, grade in student_with_grade.items():

                # Continue if student ID does not match
                if student_id != submission.student_id:
                    continue

                # Change the grade if the corresponding assignment ID and student ID are found
                submission.grade = grade
                is_modified = True

        # If the submission is not modified (i.e., does not exist in the external JSON file)
        if not is_modified:
            submission.grade = "/"


def print_all_current_submissions(filter_condition):

    """
    This function aims to print out the details of all submissions in the SUBMISSION_LIST cache.
    :param filter_condition: The filtering condition for printing submissions.
    :return: None
    """

    # Arrange submissions in SUBMISSION_LIST in ascending order
    sorted_array = sort_submission_array(Submission.SUBMISSION_LIST)
    Submission.SUBMISSION_LIST = sorted_array

    # Print all when no condition is imposed
    if filter_condition == 0:
        # Loop through the SUBMISSION_LIST array and print each submission
        for submission in Submission.SUBMISSION_LIST:
            print(" • ", end="")
            print(submission)

    # Print only graded submissions
    elif filter_condition == 1:

        # Loop through all submissions in the submission list
        for submission in Submission.SUBMISSION_LIST:

            # Continue the loop if there is grade
            if submission.grade != '/':
                continue

            # Print the submission without the grade
            print(" • ", end="")
            print(submission)


def calculate_average_score(assignment_id):

    """
    This function aims to calculate the average grade of a submission.
    :param assignment_id: The assignment ID of the submission.
    :return: A float representing the average grade of the submission.
    """

    # Empty variable to store marks, counter, and an array to store filtered submissions
    total_marks = 0
    number_of_submissions = 0
    filtered_submissions = []

    # Loop through all assignments
    for submission in Submission.SUBMISSION_LIST:

        # If "ALL" is inputted, append all submissions to the list
        if assignment_id == "ALL":
            filtered_submissions.append(submission)
            continue

        # If an individual assignment ID is inputted, append only the relevant submission
        elif submission.assignment_id == assignment_id:
            filtered_submissions.append(submission)
            continue

    # Return -1 if there are no filtered submissions
    if len(filtered_submissions) == 0:
        return -1

    # Record the details from each filtered submission
    for filtered_submission in filtered_submissions:

        # Ignore ungraded submissions
        if filtered_submission.grade == '/':
            continue

        # Calculate total marks and number of submissions
        total_marks += int(filtered_submission.grade)
        number_of_submissions += 1

    # Calculate average marks, but if there are no graded submissions, assign 0
    average_mark = total_marks / number_of_submissions if number_of_submissions > 0 else 0

    # Format marks into two decimal points
    average_mark = f"{average_mark:.2f}"
    return average_mark


def retrieve_highest_score_student():

    """
    This function aims to retrieve the highest score student for each assignment from the SUBMISSION_LIST cache.
    :return: None
    """

    # Empty variables to store top performing students
    top_performing_list = []
    is_assignment_id_exist = False

    # Retrieve each submission from SUBMISSION_LIST array
    for submission in Submission.SUBMISSION_LIST:

        # Loop through the top_performing_list array
        for added_submission in top_performing_list:

            # Continue loop if assignment ID does not match
            if submission.assignment_id != added_submission.assignment_id:
                continue

            # If assignment ID matches
            is_assignment_id_exist = True

            # Find the index of the related submission in top_performing_list
            current_index = top_performing_list.index(added_submission)

            # Try to compare grades, if the grade is higher than the stored submission, then replace it.
            # Don't worry about comparing '/' with numbers like '0'. '/' is always smaller than '0'
            if submission.grade > added_submission.grade:
                top_performing_list[current_index] = submission

            # If the grades are the same (we have to avoid ungraded submissions), then display both students
            elif submission.grade == added_submission.grade and submission.grade != '/':
                top_performing_list.insert(current_index + 1, submission)

            # End loop after finish modifying
            break

        # If the assignment ID has not been stored in the top_performing_list array, add it (initiation)
        if not is_assignment_id_exist:
            top_performing_list.append(submission)
            continue

    # If there is a submission in the array that is ungraded, change the student ID to '/' as well
    for submission in top_performing_list:
        if submission.grade == "/":
            submission.student_id = "/"

        # Print each submission in the array
        print(" • ", end="")
        print(submission)


def display_student_not_meeting_threshold(assignment_id, threshold):

    """
    This function aims to display the list of students who do not meet a threshold for a particular assignment.
    :param assignment_id: The assignment ID of the submission.
    :param threshold: The minimum mark
    :return: None
    """

    # Empty variable to store students not meeting threshold
    students_not_meeting_list = []

    # Loop through the SUBMISSION_LIST array
    for submission in Submission.SUBMISSION_LIST:

        # Skip ungraded submissions
        if submission.grade == '/':
            continue

        # Convert the threshold and submission grade to integer
        threshold = int(threshold)
        grade = int(submission.grade)

        # If the assignment ID matches and the grade is lower than the threshold, the student is recorded
        if submission.assignment_id == assignment_id and grade < threshold:
            students_not_meeting_list.append(submission)

    # Inform that there are no students lower than there threshold mark if there's nothing in the lsit
    if len(students_not_meeting_list) == 0:
        print("\nNo graded students fall below the threshold mark.\n")

    # Print the students at the end
    for submission in students_not_meeting_list:
        print(submission)


def delete_file_from_data(assignment_id, student_id):

    """
    This function aims to remove the submission from cache, remove the text file associated to it,
    and remove it from the JSON file.
    :param assignment_id: The assignment ID of the submission.
    :param student_id: The student ID of the submission.
    :return: True if operation successful, false otherwise
    """

    # We first remove the file in the Data folder
    is_deleted = remove_submission_file(assignment_id, student_id)

    if not is_deleted:
        return False

    # We then delete the record in SUBMISSION_LIST
    for submission in Submission.SUBMISSION_LIST:

        # Continue loop if doesn't meet criteria
        if submission.assignment_id != assignment_id or submission.student_id != student_id:
            continue

        # Remove submission from SUBMISSION_LIST
        Submission.SUBMISSION_LIST.remove(submission)
        break

    while True:
        # We lastly ask user whether to delete it in JSON
        update_json = input("\nDo you want to directly update the Grades JSON file (Y/N): ").lower().strip()

        # Prompt for correct input
        if update_json not in ["y", "n"]:
            print("Please enter either 'y' or 'n'.")
            continue

        # If the user does not want to update JSON
        if update_json == "n":
            print("\nThe changes are stored in cache. Run Option 11 to store your data into Grades JSON file.")
            return False

        # If the user wants to update JSON directly
        store_grade_to_file()
        return True
