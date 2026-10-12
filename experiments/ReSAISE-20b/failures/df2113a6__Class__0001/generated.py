import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom HTTP header into a response string, sanitizing the
    user-supplied value to mitigate injection attacks (CWE-74).

    Parameters:
        user_header (str): The raw value supplied by the user.

    Returns:
        str: A single HTTP header line with the sanitized value,
             terminated by CRLF.

    Notes:
        - All carriage return (CR) and line feed (LF) characters are removed
          to prevent header injection.
        - Leading/trailing whitespace is trimmed.
        - Any remaining control characters (0x00-0x1F) except TAB are removed.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Remove CR and LF to prevent header injection
    sanitized = re.sub(r'[\r\n]+', '', user_header)

    # Remove other control characters except tab (0x09)
    sanitized = re.sub(r'[\x00-\x08\x0A-\x1F]', '', sanitized)

    # Trim whitespace
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}\r\n"