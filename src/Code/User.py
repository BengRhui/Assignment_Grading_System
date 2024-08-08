from Data_IO import load_user_from_json
from Data_IO import save_user_to_json


class User:

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def __str__(self):
        information = ("----------" + "\n"
                       + "User ID: " + self.user_id + "\n"
                       + "Username: " + self.username + "\n"
                       + "Password: " + self.password + "\n"
                       + "----------")
        return information


def retrieve_user_information():

    """
    This function aims to:
    1. Convert the information stored in JSON into the User object.
    2. Store all User objects into array
    :return: User objects in array form
    """

    # Retrieve user information from load_user_from_json function
    content = load_user_from_json()

    # Empty array to store User objects
    user_list = []

    # Create all User objects
    for user_id, user_login_credentials in content.items():

        # Retrieve username and password from JSON
        login_username = user_login_credentials.get("Username", "")
        login_password = user_login_credentials.get("Password", "")

        # Create an individual User object
        user = User(user_id, login_username, login_password)
        user_list.append(user)

    # Return the stored array with all User information
    return user_list


def validate_login_details(login_username, login_password):

    """
    This function aims to validate the login credentials of a user.
    :param login_username: Username inputted by user
    :param login_password: Password inputted by user
    :return: True if the account exists, False if the account is not valid
    """

    # Retrieve the list of users
    user_list = retrieve_user_information()

    # Loop through all users and check credentials
    for user in user_list:
        if user.username == login_username and user.password == login_password:
            return True, user

    # Return False if the account does not exist
    return False, None


def create_new_user(username, password):
    """
    This function aims to create a new user and add it to the JSON file.
    :param username: New username
    :param password: New password
    :return: None
    """

    # Retrieve the username list
    user_list = retrieve_user_information()

    # Create user ID using length of user_list + 1
    new_user_id = f"{len(user_list) + 1:05d}"

    # Create new user
    new_user = User(new_user_id, username, password)

    # Update JSON file
    update_user(new_user)


def update_user(new_user):

    """
    This function aims to return an array with updated User objects with the new username and password
    :param new_user:
    :return: Array with updated User objects
    """

    # Retrieve the initial user list from the file
    user_list = retrieve_user_information()

    # Variable to store whether the new user is an existing or a new one
    is_existing = False

    # Update the corresponding existing user
    length_of_list = len(user_list)
    for index in range(length_of_list):
        if user_list[index].user_id == new_user.user_id:
            user_list[index] = new_user
            is_existing = True

    # Update new user
    if not is_existing:
        user_list.append(new_user)

    # Store into the JSON file
    save_user_to_json(user_list)
