import re

# Regular expression that matches any control character or whitespace that could break HTTP headers.
# We allow printable ASCII characters except CR (0x0D) and LF (0x0A).
# This ensures the header value cannot contain line breaks that would terminate the header field.
_HEADER_SANITIZE_RE = re.compile(r'[\r\n]')

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize a user-supplied header value and return the full HTTP header string.

    The function removes any CR or LF characters to prevent HTTP response splitting
    (CWE-74). It also strips any leading or trailing whitespace to avoid accidental
    header injection.

    Args:
        header_content (str): The raw user-provided value for the custom header.

    Returns:
        str: A properly formatted HTTP header line with the sanitized value.
    """
    # Strip leading/trailing whitespace to avoid accidental header prefixes
    cleaned = header_content.strip()

    # Remove any CR or LF characters to prevent line breaks in the header
    cleaned = _HEADER_SANITIZE_RE.sub('', cleaned)

    # Return the complete header line
    return f"X-Custom-Header: {cleaned}"