import re

# RFC 7230 token characters (excluding CTLs and separators)
TOKEN_RE = re.compile(r'^[!#$%&\'*+\-.^_`|~0-9a-zA-Z]+$')

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response, sanitizing the user supplied value.

    Parameters
    ----------
    custom_value : str
        The user supplied header value.

    Returns
    -------
    str
        A string containing the full HTTP header line, e.g.
        "X-Custom-Header: <sanitized_value>\r\n".

    Raises
    ------
    ValueError
        If the supplied value contains characters that are not allowed in an HTTP token.
    """
    if not isinstance(custom_value, str):
        raise ValueError("Header value must be a string")

    # Strip CR and LF to prevent injection
    sanitized = custom_value.replace('\r', '').replace('\n', '')

    # Ensure the value is a valid token (no separators or control characters)
    if not TOKEN_RE.fullmatch(sanitized):
        raise ValueError("Header value contains invalid characters")

    return f"X-Custom-Header: {sanitized}\r\n"