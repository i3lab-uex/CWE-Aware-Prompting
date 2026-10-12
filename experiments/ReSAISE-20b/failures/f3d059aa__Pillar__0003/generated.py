import re

# RFC‑7230 defines a header field value as any token or quoted string,
# but for simplicity we restrict it to printable US‑ASCII characters
# excluding CR and LF.
_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to an HTTP response.

    The function validates that `user_header` contains only printable
    ASCII characters (excluding CR and LF) to prevent header injection.
    If the value is invalid, a ValueError is raised.

    Parameters
    ----------
    user_header : str
        The value of the custom header supplied by a user.

    Returns
    -------
    str
        A string representing the complete HTTP header line,
        e.g. "X-Custom-Header: value\r\n".

    Raises
    ------
    ValueError
        If `user_header` contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Validate header value using the compiled regex
    if not _HEADER_VALUE_RE.fullmatch(user_header):
        raise ValueError(
            "Header value contains prohibited characters (CR, LF, non‑ASCII)"
        )

    # Build the header line
    return f"X-Custom-Header: {user_header}\r\n"