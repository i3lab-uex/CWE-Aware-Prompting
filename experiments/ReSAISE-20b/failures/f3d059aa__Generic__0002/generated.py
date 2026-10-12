import re

# Regular expression to validate that the header value contains only printable ASCII
# characters and does not include CR or LF which would break the HTTP header format.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to an HTTP response.

    Parameters
    ----------
    user_header : str
        The value of the custom header supplied by the user.

    Returns
    -------
    str
        A complete header line in the form:
            "X-User-Header: <user_header>\r\n"

    Notes
    -----
    The function performs a basic sanity check on the supplied header value.
    It ensures that no CR or LF characters are present, which would otherwise
    allow header injection.  The check uses a regular expression that permits
    any printable ASCII character (0x20‑0x7E).  If the value does not match,
    a ``ValueError`` is raised.

    Security
    --------
    By validating the header value we mitigate the risk of HTTP response
    splitting and other injection attacks.  The validation is intentionally
    conservative; more permissive checks could be added if required.
    """
    # Validate the header value
    if not HEADER_VALUE_RE.match(user_header):
        raise ValueError("Invalid header value: must contain only printable ASCII characters and no CR/LF.")

    # Construct the full header line
    return f"X-User-Header: {user_header}\r\n"