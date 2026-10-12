import re

# Allowed characters in an HTTP header field value (RFC 7230, token + visible ASCII except CTLs)
_TOKEN_CHARS = r"[A-Za-z0-9!#$%&'*+\-.^_`|~]+"

# Regex to find any character that is NOT allowed in a header value
_INVALID_CHARS_RE = re.compile(r"[^A-Za-z0-9!#$%&'*+\-.^_`|~]")

def include_custom_header(custom_value: str) -> str:
    """
    Sanitize a user supplied string and embed it in an HTTP header line.

    Parameters
    ----------
    custom_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A single header line that can safely be appended to an HTTP response.

    Notes
    -----
    * The function removes any carriage‑return or line‑feed characters to prevent CRLF injection.
    * It also strips out any character that is not part of the allowed token set for header values.
    * The returned header line ends with CRLF as required by the HTTP specification.

    Raises
    ------
    re.error
        If an internal regular expression fails (unlikely in normal operation).
    """
    # Remove CR and LF to avoid header injection
    sanitized = custom_value.replace("\r", "").replace("\n", "")

    # Replace any disallowed character with an empty string
    sanitized = _INVALID_CHARS_RE.sub("", sanitized)

    # Ensure the value is not empty after sanitization
    if not sanitized:
        sanitized = "default"

    # Construct the header line
    return f"X-Custom-Header: {sanitized}\r\n"