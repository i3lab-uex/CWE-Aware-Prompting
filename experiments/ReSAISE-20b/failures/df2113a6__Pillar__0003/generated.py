import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response after sanitizing the user-provided value.

    Parameters
    ----------
    user_header : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A properly formatted header line including CRLF terminator.
    
    Notes
    -----
    - The function removes any carriage return or line feed characters from the input to prevent
      HTTP response splitting attacks.
    - Leading and trailing whitespace is stripped to avoid accidental header injection.
    """
    # Remove CRLF characters that could break the HTTP protocol
    sanitized = re.sub(r'[\r\n]+', '', user_header)
    
    # Strip surrounding whitespace
    sanitized = sanitized.strip()
    
    # Return the header line with CRLF termination
    return f"X-Custom-Header: {sanitized}\r\n"