import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a sanitized custom header into an HTTP response.

    The returned string is in the form:
        "X-Custom-Header: <sanitized_value>\r\n"

    Parameters
    ----------
    user_header : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A complete HTTP header line with the sanitized value.
    """
    # Remove any CR or LF characters to prevent injection
    sanitized = re.sub(r'[\r\n]+', '', user_header)

    # Optionally strip leading/trailing whitespace
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}\r\n"