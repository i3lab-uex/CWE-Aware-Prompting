import re

# RFC 7230 header field value must not contain CR or LF.
# We allow printable ASCII characters (0x20-0x7E) and tab (0x09).
# Anything else is stripped out to prevent injection or header
# injection attacks (CWE-707).
HEADER_VALUE_PATTERN = re.compile(r'[^ \t\x21-\x7E]+')

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize a user-supplied header value and return the final
    custom header string ready to be inserted into an HTTP response.

    Parameters
    ----------
    header_content : str
        The raw user-supplied header value.

    Returns
    -------
    str
        A safe, sanitized header string of the form:
        "X-Custom-Header: <sanitized_value>"
    """
    # Strip any CR or LF characters that could split the header.
    sanitized = HEADER_VALUE_PATTERN.sub('', header_content)

    # Ensure the header is not empty after sanitization.
    if not sanitized:
        sanitized = 'default'

    return f"X-Custom-Header: {sanitized}"