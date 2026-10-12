import re

# Regex pattern that matches a valid HTTP header value.
# It allows printable ASCII characters except CR, LF, and colon (':').
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E&&[^:\r\n]]+$')

def add_custom_header(header_value: str) -> str:
    """
    Return a complete HTTP header line with the provided custom header value.
    
    The function validates that `header_value` contains only characters
    permitted in HTTP header values, preventing CRLF injection and other
    header injection attacks. If the value does not match the pattern,
    a ValueError is raised.
    
    Parameters
    ----------
    header_value : str
        The custom header value supplied by the user.
    
    Returns
    -------
    str
        A string in the form 'Custom-Header: <header_value>\r\n'.
    
    Raises
    ------
    ValueError
        If `header_value` contains disallowed characters.
    """
    if not isinstance(header_value, str):
        raise ValueError("Header value must be a string")

    # Ensure the header value does not contain CR, LF or colon.
    if not _HEADER_VALUE_RE.match(header_value):
        raise ValueError("Invalid characters in header value")

    # Construct the header line safely.
    return f"Custom-Header: {header_value}\r\n"