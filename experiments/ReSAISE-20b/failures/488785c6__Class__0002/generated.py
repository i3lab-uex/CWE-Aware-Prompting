import re

# Allowed characters: printable ASCII except CR (\\r) and LF (\\n).
_ALLOWED_CHARS_RE = re.compile(r'^[\x20-\x7E]+$')

def add_safe_header(custom_value: str) -> str:
    """
    Sanitize a user‑supplied header value and return the full HTTP header line.

    The function removes any control characters that could be used for CRLF injection
    and ensures the value only contains printable ASCII characters.  If the value does
    not match the allowed pattern, it is silently replaced with an empty string.

    Parameters:
        custom_value (str): The raw header value supplied by the user.

    Returns:
        str: A well‑formed HTTP header line, e.g. "X-Custom-Header: value".
    """
    # Strip leading/trailing whitespace to avoid accidental injection
    cleaned = custom_value.strip()

    # Reject values containing CR or LF (0x0D, 0x0A) entirely
    if '\r' in cleaned or '\n' in cleaned:
        cleaned = ''

    # Validate against allowed character set
    if not _ALLOWED_CHARS_RE.match(cleaned):
        cleaned = ''

    return f"X-Custom-Header: {cleaned}"