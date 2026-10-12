import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Safely insert a user-provided value into an HTTP response header.

    The function removes any carriage-return, line-feed or other control
    characters that could lead to HTTP Response Splitting (CWE‑74).  It also
    strips non-printable characters and limits the value to a single line.

    Parameters:
        custom_header_value (str): The raw header value supplied by the user.

    Returns:
        str: A complete HTTP header line with the sanitized value.
    """
    # 1. Remove CR, LF and any other control characters that could break the header
    sanitized = re.sub(r'[\r\n]', '', custom_header_value)

    # 2. Remove any non-printable characters except standard whitespace
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # 3. Collapse multiple spaces into a single space to avoid header ambiguity
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # 4. Ensure the header is a single line
    sanitized = sanitized.replace('\n', '').replace('\r', '')

    return f"X-Custom-Header: {sanitized}"