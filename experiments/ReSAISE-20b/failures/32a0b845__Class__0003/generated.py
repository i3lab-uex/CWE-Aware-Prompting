import re

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom HTTP header into the response headers.

    The function sanitizes the user-supplied `header_content` by removing any
    carriage‑return or line‑feed characters that could be used for CRLF injection,
    which would otherwise allow an attacker to inject additional headers or
    manipulate the response.

    Parameters
    ----------
    header_content : str
        The raw value supplied by the user for the custom header.

    Returns
    -------
    str
        A complete header line suitable for inclusion in an HTTP response,
        e.g. "X-Custom-Header: sanitized_value\r\n".

    Raises
    ------
    re.error
        If the regular expression used for sanitization fails (unlikely in this
        simple pattern).
    """
    # Remove any CR or LF characters to prevent header injection.
    sanitized = re.sub(r'[\r\n]', '', header_content)

    # Construct the full header line (using CRLF as per RFC 7230).
    return f"X-Custom-Header: {sanitized}\r\n"