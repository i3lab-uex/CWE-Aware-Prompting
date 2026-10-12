import re

# Regular expression for a safe HTTP header value.
# Allows printable ASCII characters except CR (\\r) and LF (\\n).
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')


def append_user_header(user_header: str) -> str:
    """
    Construct an HTTP header line with a user‑supplied value, ensuring the
    value is safe for inclusion in HTTP responses.

    The header format used here is:
        X-Custom-Header: <user_header>

    Parameters
    ----------
    user_header : str
        The value supplied by the caller. It must contain only printable ASCII
        characters (0x20‑0x7E). CR (`\r`) and LF (`\n`) are explicitly disallowed
        to prevent header injection (CWE‑74).

    Returns
    -------
    str
        The complete header line ready to be added to an HTTP response.

    Raises
    ------
    ValueError
        If `user_header` contains disallowed characters.
    """
    # Reject empty or None values
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Ensure the header does not contain CR or LF
    if '\r' in user_header or '\n' in user_header:
        raise ValueError("Header value contains disallowed CR or LF characters")

    # Verify the header matches the allowed pattern
    if not SAFE_HEADER_VALUE_RE.match(user_header):
        raise ValueError("Header value contains invalid characters")

    # Construct the header line
    return f"X-Custom-Header: {user_header}"