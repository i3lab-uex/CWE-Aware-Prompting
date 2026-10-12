import re

# Regular expression that matches a safe HTTP header field value.
# Allows printable ASCII characters except control chars and CR/LF.
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def include_custom_header(custom_value: str) -> str:
    """
    Return a full HTTP header string with the user supplied value inserted
    into a custom header field. The value is validated against a regular
    expression that permits only printable ASCII characters (excluding CR/LF).

    Parameters
    ----------
    custom_value : str
        The user supplied value for the header.

    Returns
    -------
    str
        A string in the form "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If the supplied value contains characters that are not allowed in a
        HTTP header field.
    """
    if not isinstance(custom_value, str):
        raise ValueError("Header value must be a string")

    if not SAFE_HEADER_VALUE_RE.match(custom_value):
        raise ValueError("Header value contains disallowed characters")

    return f"X-Custom-Header: {custom_value}\r\n"