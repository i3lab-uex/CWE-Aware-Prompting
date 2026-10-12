import re

# Allowed characters for a header value: token + visible ASCII except control chars and CRLF
_HEADER_VALUE_RE = re.compile(r'^[\x21-\x7E]+$')

def add_response_header(response_header: str) -> str:
    """
    Safely prepend a custom header to an HTTP response.

    Parameters
    ----------
    response_header : str
        The value supplied by the user for a custom header.

    Returns
    -------
    str
        A complete HTTP header line: "X-Custom-Header: <value>".

    Notes
    -----
    The function validates that the header value contains only printable ASCII
    characters (0x21–0x7E). This prevents CRLF injection and ensures the header
    is well‑formed, mitigating CWE‑707.
    """
    if not isinstance(response_header, str):
        raise TypeError("Header value must be a string")

    # Strip surrounding whitespace to avoid accidental injection
    cleaned = response_header.strip()

    # Validate the cleaned value against allowed characters
    if not _HEADER_VALUE_RE.fullmatch(cleaned):
        raise ValueError("Invalid header value: contains disallowed characters")

    return f"X-Custom-Header: {cleaned}"