import re

# RFC 7230 token definition (simplified)
_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-zA-Z]+$")

# RFC 7230 quoted-string definition (simplified)
_QUOTED_STRING_RE = re.compile(r'^"([^"\r\n\\]|\\[tbnrfv\\"])*"$')

def _sanitize_header_value(value: str) -> str:
    """
    Ensure the header value is safe for HTTP headers.
    Reject any CR/LF characters to prevent injection attacks.
    Accept either a token or a quoted-string as defined by RFC 7230.
    """
    if "\r" in value or "\n" in value:
        raise ValueError("Header value contains forbidden CR/LF characters")

    # Allow token or quoted-string
    if _TOKEN_RE.match(value) or _QUOTED_STRING_RE.match(value):
        return value
    raise ValueError("Header value contains invalid characters")

def insert_custom_header(custom_header: str) -> str:
    """
    Construct a complete HTTP header line containing the custom header value.

    Args:
        custom_header: The user-provided header value (string).

    Returns:
        A string in the form 'Custom-Header: <value>\r\n'.

    Raises:
        ValueError: If the header value contains disallowed characters or
                    line breaks that could lead to injection.
    """
    # Sanitize the input value
    safe_value = _sanitize_header_value(custom_header)

    # Construct and return the header line
    return f"Custom-Header: {safe_value}\r\n"