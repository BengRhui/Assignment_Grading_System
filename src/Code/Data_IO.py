import json
import os


def load_user_from_json():

    """
    This function loads the user login credentials from the User_Credentials.json file
    :return: dictionary / JSON with user credentials
    """

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    json_file_directory = os.path.join(parent_directory, "Data/User_Credentials.json")

    # Open User_Credentials.json file
    json_file = open(json_file_directory, "r")

    # Read and return contents from JSON file
    content = json.loads(json_file.read())

    # Close file
    json_file.close()
    return content


def save_user_to_json(user_list):

    """
    This function saves the user login credentials to the User_Credentials.json file
    :param user_list:
    :return:
    """

    # Initialize a dictionary to store data
    data = {}

    # Retrieve data from list to dictionary
    for user in user_list:
        individual_user = {
            user.user_id: {
                "Username": user.username,
                "Password": user.password
            }
        }
        data.update(individual_user)

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    json_file_directory = os.path.join(parent_directory, "Data/User_Credentials.json")

    # Open User_Credentials.json file
    json_file = open(json_file_directory, "w")

    # Update contents of JSON file
    json_file.write(json.dumps(data))

    # Close file
    json_file.close()


def retrieve_submission_grade_from_file(student_id, assignment_id):

    """
    This function retrieves the submission grade from the JSON file.
    :param student_id: The student ID associated with the assignment.
    :param assignment_id: The ID of the assignment.
    :return: An integer if grade is available, else '/'.
    """

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    json_file_directory = os.path.join(parent_directory, "Data/Grades.json")

    # Open Grades.json file
    json_file = open(json_file_directory, "r")

    # Retrieve the contents from the JSON file
    marks = json.loads(json_file.read())

    # Close file
    json_file.close()

    # Retrieve the assignment marks for all students from the dictionary
    assignment_marks = marks.get(assignment_id, '')

    # Return '/' if the mark does not exist
    if assignment_marks == '':
        return '/'

    # Retrieve the mark for the corresponding student
    corresponding_marks = assignment_marks.get(student_id, '/')

    # Convert marks into string to avoid concatenation issues
    corresponding_marks = str(corresponding_marks)
    return corresponding_marks


def load_grades_into_json(data):

    """
    This function loads the submission grades into the JSON file.
    :param data: Submission information stored in dictionary format.
    :return: None
    """

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    json_file_directory = os.path.join(parent_directory, "Data/Grades.json")

    # Open Grades.json file
    json_file = open(json_file_directory, "w")

    # Write the contents into the JSON file
    json_file.write(json.dumps(data))

    # Close file
    json_file.close()


def remove_submission_file(assignment_id, student_id):

    """
    This function removes the associated submission file from the Data folder.
    :param assignment_id: Assignment ID associated with the assignment.
    :param student_id: Student ID associated with the assignment.
    :return: False if the file is not found, true if the file is deleted.
    """

    # Form the name of the text file
    file_name = student_id + "_" + assignment_id + ".txt"

    # Navigate to the correct directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    text_file_directory = os.path.join(parent_directory, "Data/" + file_name)

    # Check if the path exists
    if os.path.exists(text_file_directory):

        # Remove and return True after the file is deleted
        os.remove(text_file_directory)
        return True

    # Return False if the file does not exist
    return False


def sort_submission_array(submission_array):

    """
    This function sorts the submission according to the assignment ID (primary), followed by student ID (secondary).
    :param submission_array: The array to be sorted
    :return: A sorted submission array
    """

    # Ensure that the array is not empty
    if len(submission_array) == 0:
        return submission_array

    # Empty variable to hold the first element
    sorted_array = [submission_array[0]]

    # Loop through the upcoming submission objects
    for submission_array_index in range(1, len(submission_array)):

        # First condition: The assignment ID is the smallest
        if submission_array[submission_array_index].assignment_id < sorted_array[0].assignment_id:
            sorted_array.insert(0, submission_array[submission_array_index])
            continue

        # Second condition: The assignment ID is the largest
        if submission_array[submission_array_index].assignment_id > sorted_array[-1].assignment_id:
            sorted_array.append(submission_array[submission_array_index])
            continue

        for sorted_index in range(len(sorted_array)):

            # Third condition: The assignment ID has already been recorded
            if sorted_array[sorted_index].assignment_id == submission_array[submission_array_index].assignment_id:

                # Condition 3.1: The student ID is the smallest
                if submission_array[submission_array_index].student_id < sorted_array[sorted_index].student_id:
                    sorted_array.insert(sorted_index, submission_array[submission_array_index])
                    break

                # Condition 3.2.1: The student ID is the largest, and it is located at the last
                if (submission_array[submission_array_index].student_id > sorted_array[sorted_index].student_id
                        and sorted_index == len(sorted_array) - 1):
                    sorted_array.append(submission_array[submission_array_index])
                    break

                # Condition 3.2.2: The student ID is the largest, and it is not located at the last
                if (sorted_array[sorted_index].student_id < submission_array[submission_array_index].student_id and
                        sorted_array[sorted_index + 1].assignment_id !=
                        submission_array[submission_array_index].assignment_id):
                    sorted_array.insert(sorted_index + 1, submission_array[submission_array_index])
                    break

                # Condition 3.3: The student ID is in the middle
                if (sorted_array[sorted_index].student_id
                        < submission_array[submission_array_index].student_id
                        < sorted_array[sorted_index + 1].student_id):
                    sorted_array.insert(sorted_index + 1, submission_array[submission_array_index])
                    break

            # Fourth condition: The assignment ID is not recorded, but it is located at the middle
            if (sorted_array[sorted_index].assignment_id
                    < submission_array[submission_array_index].assignment_id
                    < sorted_array[sorted_index + 1].assignment_id):
                sorted_array.insert(sorted_index + 1, submission_array[submission_array_index])
                break

    # Return the sorted array
    return sorted_array
