import re

# Regular expression that matches a valid HTTP header field value.
# RFC 7230 allows any VCHAR (visible ASCII) and obs-text, but for safety we restrict to
# printable characters excluding control chars and the CR/LF line breaks.
_HEADER_VALUE_RE = re.compile(r'^[\x21-\x7E\x80-\xFF]*$')

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    Parameters
    ----------
    user_header : str
        The value provided by the user for the custom header.

    Returns
    -------
    str
        A string representing the full header line, e.g.
        "X-Custom-Header: <sanitized_value>\r\n"

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise ValueError("Header value must be a string")

    # Strip leading/trailing whitespace to avoid accidental CRLF injection.
    sanitized = user_header.strip()

    # Ensure the value does not contain line breaks or control characters.
    if not _HEADER_VALUE_RE.match(sanitized):
        raise ValueError("Header value contains disallowed characters")

    # Construct the header line with a standard CRLF terminator.
    return f"X-Custom-Header: {sanitized}\r\n"