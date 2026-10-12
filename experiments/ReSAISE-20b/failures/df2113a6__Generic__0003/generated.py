import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom HTTP header with the given user-provided value.

    The function sanitizes the input to ensure it contains only printable ASCII
    characters (code points 32–126) and does not include carriage return or line feed
    characters, which would otherwise break the HTTP header format.

    Parameters:
        user_header (str): The raw value supplied by the user.

    Returns:
        str: A complete header string of the form
             "X-Custom-Header: <sanitized_value>".
    """
    # Regular expression to match any character that is NOT a printable ASCII
    # character (32-126) or CR/LF. We replace those characters with an empty string.
    # Note: re.ASCII ensures that \w etc. are ASCII only.
    sanitized = re.sub(r'[^\x20-\x7E]', '', user_header, flags=re.ASCII)

    # Additionally strip any CR or LF that might slip through.
    sanitized = re.sub(r'[\r\n]', '', sanitized)

    # If the sanitized value is empty, use a safe default.
    if not sanitized:
        sanitized = "default"

    return f"X-Custom-Header: {sanitized}"