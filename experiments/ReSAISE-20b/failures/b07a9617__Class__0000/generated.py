import re

# RFC 7230 token characters (alphanumerics and allowed separators)
_TOKEN_RE = re.compile(r'^[!#$%&\'*+\-.^_`|~0-9a-zA-Z]+$')

def _sanitize_header_value(value: str) -> str:
    """
    Remove any CRLF sequences and ensure the value contains only token characters.
    If the value does not match the allowed pattern, it is replaced with an empty string.
    """
    # Remove any CR or LF characters to prevent header injection
    value = re.sub(r'[\r\n]+', '', value)

    # Strip leading/trailing whitespace
    value = value.strip()

    # Validate against token pattern; if invalid, neutralize to empty string
    if not _TOKEN_RE.match(value):
        return ''
    return value

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Construct a safe custom HTTP header string.

    Parameters
    ----------
    custom_header_value : str
        User-supplied value for the custom header.

    Returns
    -------
    str
        A complete HTTP header line in the form:
            X-Custom-Header: <sanitized_value>
    """
    sanitized = _sanitize_header_value(custom_header_value)
    return f"X-Custom-Header: {sanitized}"