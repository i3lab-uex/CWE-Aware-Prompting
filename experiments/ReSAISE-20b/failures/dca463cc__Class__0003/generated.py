import re

# Regular expression that matches a safe header value:
# - only printable ASCII characters (excluding CR and LF)
# - no control or non‑printable characters
SAFE_HEADER_RE = re.compile(r'^[\x20-\x7E]+$')

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom HTTP header into the response headers.

    Parameters
    ----------
    custom_header : str
        The user‑supplied header value. It must contain only printable ASCII
        characters (no CR or LF). The function validates this using a regular
        expression to mitigate header injection attacks (CWE‑74).

    Returns
    -------
    str
        A string containing the full header line, e.g.
        "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If `custom_header` contains disallowed characters or is empty.
    """
    # Ensure the header value is a non‑empty string
    if not isinstance(custom_header, str) or not custom_header:
        raise ValueError("custom_header must be a non‑empty string")

    # Validate against the safe pattern
    if not SAFE_HEADER_RE.match(custom_header):
        raise ValueError(
            "custom_header contains disallowed characters (CR, LF, control chars)"
        )

    # Construct the header line safely
    return f"X-Custom-Header: {custom_header}\r\n"