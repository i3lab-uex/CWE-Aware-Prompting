import re

# Regular expression that matches a valid HTTP header field value.
# According to RFC 7230, a header field value can contain visible ASCII
# characters (octets 32-126) and optional linear whitespace.
# For simplicity we allow letters, digits, punctuation (excluding control
# characters and CRLF), and spaces/tabs.  This prevents injection of
# line breaks that could lead to HTTP response splitting (CWE‑700/707).
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]+$')

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    Parameters
    ----------
    custom_value : str
        User-provided value for the header.  Must contain only visible ASCII
        characters (32–126) to avoid injection of control characters.

    Returns
    -------
    str
        A header line suitable for inclusion in an HTTP response, e.g.
        "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If the supplied value contains characters that are not allowed in an
        HTTP header field value.
    """
    # Strip leading/trailing whitespace that might be accidental but
    # preserve internal spaces.
    sanitized = custom_value.strip()

    if not HEADER_VALUE_RE.match(sanitized):
        raise ValueError(
            "Custom header value contains invalid characters. "
            "Only visible ASCII (32–126) is allowed."
        )

    # Build the header line.  The CRLF terminator is required by HTTP.
    return f"X-Custom-Header: {sanitized}\r\n"