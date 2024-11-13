# utils/file_utils.py

import re

def to_snakecase(text: str) -> str:
    """
    Converts a string to snake_case.
    Example: 'Column Name' -> 'column_name'
    """
    # Replace spaces with underscores, remove special characters, and make lowercase
    text = re.sub(r'[\W]+', '_', text).strip().lower()
    return text

def to_titlecase(text: str) -> str:
    """
    Converts a string to Title Case.
    Example: 'column_name' -> 'Column Name'
    """
    # Split by underscores, capitalize each word, and join with spaces
    text = text.replace('_', ' ')
    return text.title()
