import os


def create_directory(path):
    """
    Create a directory at the specified path if it doesn't already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
