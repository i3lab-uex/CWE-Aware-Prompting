import re

# Regular expression that matches only printable ASCII characters (space to ~).
# This excludes control characters, newlines, and other potentially dangerous bytes.
_VALID_HEADER_RE = re.compile(r'^[\x20-\x7E]+$')

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    Parameters
    ----------
    header_content : str
        The user-provided value for the custom header. It must contain only
        printable ASCII characters (space to tilde). This restriction prevents
        injection of control or non‑printable bytes that could break the HTTP
        protocol.

    Returns
    -------
    str
        A complete header line including the custom header and a trailing CRLF.

    Raises
    ------
    ValueError
        If `header_content` contains characters outside the allowed range.
    """
    if not isinstance(header_content, str):
        raise ValueError("Header content must be a string")

    # Sanitize: ensure the header value is well‑formed.
    if not _VALID_HEADER_RE.match(header_content):
        raise ValueError(
            "Header content contains invalid characters; only printable ASCII "
            "(space to ~) is allowed."
        )

    # Construct the header line. The header name can be fixed (e.g., X-Custom-Header)
    # or you could allow a custom name; here we keep it constant for safety.
    return f"X-Custom-Header: {header_content}\r\n"