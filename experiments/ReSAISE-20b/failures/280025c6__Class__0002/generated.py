import re

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize a user supplied header value and construct a custom HTTP header.

    The function removes any control characters (including CRLF) that could be
    used to terminate the header line or inject additional headers.  Only
    printable ASCII characters (codes 32–126) are retained; everything else is
    stripped.  The sanitized value is then returned as a complete header line.

    Parameters
    ----------
    header_content : str
        The raw user supplied header value.

    Returns
    -------
    str
        A sanitized header line in the form "X-Custom: <value>".
    """
    # Remove CR, LF and any non-printable ASCII characters
    sanitized = re.sub(r"[^\x20-\x7E]+", "", header_content)

    # Ensure the value is not empty; fall back to a safe default
    if not sanitized:
        sanitized = "default"

    return f"X-Custom: {sanitized}"