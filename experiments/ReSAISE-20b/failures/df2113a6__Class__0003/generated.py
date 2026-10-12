import re

# Allowed characters: printable ASCII except CR (\\r) and LF (\\n)
_ALLOWED_CHARS_RE = re.compile(r'[\x20-\x7E]')

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom HTTP header with the given user-supplied value after sanitizing it.

    The function removes any characters that are not printable ASCII (0x20–0x7E),
    which prevents CRLF injection and other header manipulation attacks.

    Parameters
    ----------
    user_header : str
        The raw value supplied by the user for the custom header.

    Returns
    -------
    str
        A full HTTP header line, e.g. "X-Custom-Header: <sanitized_value>".

    Raises
    ------
    re.error
        If the regular expression compilation or matching fails (unlikely).
    """
    # Ensure input is a string; if not, convert to str
    value = str(user_header)

    # Filter out any non‑printable or control characters (including CR and LF)
    sanitized = ''.join(_ALLOWED_CHARS_RE.findall(value))

    # Construct the header line
    return f"X-Custom-Header: {sanitized}"