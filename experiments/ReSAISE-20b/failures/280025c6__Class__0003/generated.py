import re

# RFC 7230 tchar characters allowed in HTTP header values (excluding CRLF)
_TCHAR_RE = re.compile(r'[^!#$%&\'*+\-.^_`|~0-9a-zA-Z]')

def inject_custom_header(header_content: str) -> str:
    """
    Insert a user-supplied value as a custom HTTP header after sanitizing it.

    The function removes any characters that are not allowed in an HTTP
    header value (RFC 7230) and strips line breaks that could be used for
    CRLF injection attacks.

    Parameters
    ----------
    header_content : str
        The raw user-provided header value.

    Returns
    -------
    str
        A single header line of the form "X-Custom-Header: <sanitized value>".
    """
    # Remove CR, LF and any other control characters
    sanitized = header_content.replace('\r', '').replace('\n', '')

    # Remove disallowed characters
    sanitized = _TCHAR_RE.sub('', sanitized)

    return f"X-Custom-Header: {sanitized}"