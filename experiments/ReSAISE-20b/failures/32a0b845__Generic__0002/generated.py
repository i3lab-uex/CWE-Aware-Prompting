import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    Parameters
    ----------
    header_content : str
        The user-supplied value for the custom header.

    Returns
    -------
    str
        A string containing a single HTTP header line:
        "X-Custom-Header: <sanitized_value>\r\n"

    Notes
    -----
    The function removes any carriage return, line feed or control characters
    from the supplied header value to prevent HTTP response splitting attacks.
    """
    # Remove CR, LF and other control characters (0x00-0x1F and 0x7F)
    sanitized = re.sub(r'[\r\n\x00-\x1F\x7F]', '', header_content)

    # Ensure the value is not empty after sanitization
    if not sanitized:
        raise ValueError("Header content must contain at least one printable character")

    return f"X-Custom-Header: {sanitized}\r\n"