import re

# Regular expression that matches a safe HTTP header value.
# Only printable ASCII characters except CR and LF are allowed.
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to an HTTP response while preventing CRLF injection.

    Parameters
    ----------
    user_header : str
        The custom header value supplied by the user.  It must contain only
        printable ASCII characters and must not include CR (`\r`) or LF (`\n`).

    Returns
    -------
    str
        The complete header line, e.g. "X-Custom-Header: value\r\n".

    Notes
    -----
    This function performs strict validation to mitigate CWE‑707 and related
    injection vulnerabilities.  It does not raise exceptions explicitly; instead,
    if the input fails validation it returns a minimal safe header.
    """
    # Validate that the header contains only allowed characters
    if not _HEADER_VALUE_RE.fullmatch(user_header):
        # If validation fails, return an empty header line to avoid injection.
        # Alternatively, you could log the incident or raise a custom exception
        # depending on application requirements.
        return ''

    # Construct the safe header line.  We use a single colon and a space
    # as per RFC 7230, followed by the sanitized value and CRLF.
    return f"X-Custom-Header: {user_header}\r\n"