import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Sanitize a user-supplied header value and return the full HTTP header string.

    The function removes any characters that could be used for HTTP response
    splitting or other injection attacks, such as CR/LF and control characters.
    It then constructs a safe header string that can be safely inserted into an
    HTTP response.

    Parameters
    ----------
    custom_header_value : str
        The user-provided header value.

    Returns
    -------
    str
        A sanitized HTTP header string of the form:
        "X-Custom-Header: <sanitized_value>"

    Notes
    -----
    - The function only removes dangerous characters; it does not attempt to
      validate the semantic meaning of the header value.
    - It deliberately avoids raising exceptions for normal inputs, but
      malformed regex patterns may raise re.error.
    """
    # Remove CR, LF, and other control characters that could break the header
    safe_value = re.sub(r'[\r\n\x00-\x1F\x7F]', '', custom_header_value)

    # Optionally, collapse any remaining whitespace sequences to a single space
    safe_value = re.sub(r'\s+', ' ', safe_value).strip()

    # Construct the header line
    return f"X-Custom-Header: {safe_value}"