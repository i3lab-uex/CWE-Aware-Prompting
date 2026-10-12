import re

# Regular expression that matches a safe header value.
# It allows printable ASCII characters except CR and LF to prevent
# HTTP response splitting or header injection.
_SAFE_HEADER_RE = re.compile(r'^[\x20-\x7E]*$')

def add_custom_header(header_value: str) -> str:
    """
    Construct an HTTP header line with a user supplied value, ensuring
    that the value cannot break the response format.

    Parameters
    ----------
    header_value : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A complete HTTP header line including a trailing CRLF, e.g.
        "X-Custom-Header: <value>\r\n".

    Notes
    -----
    The function explicitly checks that the value contains only printable
    ASCII characters (space through tilde) and rejects any CR or LF
    characters.  This mitigates CWE-74 (HTTP response splitting / header
    injection) by neutralising special elements that could be interpreted
    by downstream HTTP clients.
    """
    if not isinstance(header_value, str):
        raise TypeError("header_value must be a string")

    # Ensure the value contains only safe characters
    if not _SAFE_HEADER_RE.fullmatch(header_value):
        raise ValueError("header_value contains disallowed characters")

    # Construct the header line with a standard name
    return f"X-Custom-Header: {header_value}\r\n"