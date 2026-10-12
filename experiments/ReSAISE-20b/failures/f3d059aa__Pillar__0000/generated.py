import re

# Regular expression that matches a valid HTTP token (RFC 7230 §3.2.6)
# This pattern allows only characters that are safe for header values.
_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


def append_user_header(user_header: str) -> str:
    """
    Build a custom HTTP header string from a user-provided value.

    The function validates that *user_header* contains only characters
    allowed by the HTTP token definition.  Any control characters,
    whitespace, or CRLF sequences are rejected to prevent
    header injection attacks (CWE‑707).

    Parameters
    ----------
    user_header : str
        The custom header value supplied by the caller.

    Returns
    -------
    str
        A full HTTP header line, e.g. "X-Custom-Header: <value>\r\n".

    Raises
    ------
    TypeError
        If *user_header* is not a string.
    ValueError
        If the header value contains invalid characters or attempts to inject CRLF.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Reject any CR or LF characters to avoid header injection.
    if "\r" in user_header or "\n" in user_header:
        raise ValueError("header value must not contain CR or LF characters")

    # Validate against the token regex.
    if not _TOKEN_RE.match(user_header):
        raise ValueError("header value contains invalid characters")

    # Construct the header line with a safe CRLF terminator.
    return f"X-Custom-Header: {user_header}\r\n"