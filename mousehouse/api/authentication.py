import hashlib
import os
from utils.logger import get_logger
from flask_restful import request
from .url_api import abort_400
from werkzeug.security import generate_password_hash, check_password_hash

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
            abort_400("User and password are nothing.", 401)
        if is_correct_user(user_data.username, user_data.password) == False:
           abort_400("Invalid user or password.", 401)
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
    hashed_pass = get_password(user_name)
    return check_password_hash(hashed_pass, password)

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
        abort_400("There is no user information file. Request cannot be accepted.", 401)
        logger.error("There is no user information file. Check data/.user file!")
    for user in users_pass:
        name = user.split(' ')[0]
        password = user.split(' ')[1]
        if name == user_name:
            return password.rstrip('\n')
    return None

def add_users(user, password):
    """
    Add mousehouse user.
    It cannot be used now because it is not incorporated.
    Probably no exception due to authentication.


    Args:
        user (str) : user
        password (str) : password
    """
    hashed_pass = generate_password_hash(password)
    try:
        with open(pass_path, 'a') as f:
            f.write('{0} {1}\n'.format(user, hashed_pass))
    except FileNotFoundError:
        abort_400("There is no user information file. Request cannot be accepted.",401)
        logger.error("There is no user information file. Check data/.user file!")