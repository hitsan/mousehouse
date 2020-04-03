import hashlib
import os
from utils.logger import get_logger
from flask_restful import request
from .url_api import abort_404

path = os.path.abspath(__file__)
pass_path = path[:-22] + '/data/.users'
logger = get_logger(__name__)
def authenticate(func):
    """
    Authentication on request.
    This function is a decorator used in REST API.
    """
    def preprocess(*args, **kwargs):
        """
        Authentication before REST API request.
        """
        user_data = request.authorization
        if user_data is None:
            abort_404("User and password are nothing.")
        if is_correct_user(user_data.username, user_data.password) == False:
           abort_404("Invalid user or password.")
        response = func(*args, **kwargs)
        return response
    return preprocess

def is_correct_user(user_name, password):
    """
    Correcte username and password.

    Args:
        user_name (str) : username
        password (str) : password

    Returns:
        bool : Return Ture if password matches, otherwise False.
    """
    hashed_pass = hashlib.sha512(password.encode()).hexdigest()
    return True if get_password(user_name) == hashed_pass else False

def get_password(user_name):
    """
    Send the password corresponding to the user name.

    Args:
        user_name (str) : username

    Returns:
        str : Returns the password associated with the user name, otherwise returns None.
    """
    try:
        with open(pass_path, 'r') as f:
            users_pass = f.readlines()
    except FileNotFoundError:
        abort_404("There is no user information file. Request cannot be accepted.")
        logger.error("There is no user information file. Check data/.user file!")
    for user in users_pass:
        name = user.split(':')[0]
        password = user.split(':')[1]
        if name == user_name:
            return password.rstrip('\n')
    return None

def add_users(user, password):
    """
    Add mousehouse user.
    It cannot be used now because it is not incorporated.


    Args:
        user (str) : user
        password (str) : password
    """
    hashed_pass = hashlib.sha512(password.encode()).hexdigest()
    with open(pass_path, 'a') as f:
        f.write('{0}:{1}\n'.format(user, hashed_pass))
