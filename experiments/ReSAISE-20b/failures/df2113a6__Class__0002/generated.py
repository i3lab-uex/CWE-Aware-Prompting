import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a sanitized custom header into an HTTP response.

    Parameters
    ----------
    user_header : str
        The raw value supplied by the user for the custom header.

    Returns
    -------
    str
        A string containing the full header line, e.g.
        "X-Custom-Header: <sanitized_value>\r\n".

    Notes
    -----
    The function sanitizes the input by:
        * Removing CR (`\r`) and LF (`\n`) characters to prevent
          header injection (CWE-74).
        * Replacing any character not in the allowed set
          of token characters with an empty string.
        * Trimming leading and trailing whitespace.

    Allowed token characters are based on RFC 7230 (section 3.2.6):
        ALPHA / DIGIT / "!#$%&'*+-.^_`|~"
    """
    # Remove CR and LF to prevent header injection
    sanitized = user_header.replace('\r', '').replace('\n', '')

    # Define allowed characters for an HTTP header value
    # We permit the token set and spaces (to allow normal values).
    allowed_pattern = re.compile(r'[^A-Za-z0-9!#$%&\'*+\-.^_`|~\s]')

    # Remove any disallowed characters
    sanitized = allowed_pattern.sub('', sanitized)

    # Trim surrounding whitespace
    sanitized = sanitized.strip()

    # Construct the full header line with CRLF termination
    return f"X-Custom-Header: {sanitized}\r\n"