import re

# Regular expression that matches a string consisting only of printable US‑ASCII characters
# (space through tilde) and disallows CR, LF, or any control characters.
_VALID_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_header : str
        The value of the custom header provided by the user.

    Returns
    -------
    str
        A complete header line in the form "Custom-Header: <value>".

    Notes
    -----
    - The function sanitises the input to prevent CRLF injection and other
      header‑related attacks.  It only accepts printable US‑ASCII characters.
    - If the input does not match the allowed pattern, an empty header value is
      used to avoid sending malformed data.
    """
    # Strip any leading/trailing whitespace that might hide injection attempts
    value = custom_header.strip()

    # Validate against the allowed pattern. If it fails, replace with an empty string.
    if not _VALID_HEADER_VALUE_RE.fullmatch(value):
        value = ""

    return f"Custom-Header: {value}"