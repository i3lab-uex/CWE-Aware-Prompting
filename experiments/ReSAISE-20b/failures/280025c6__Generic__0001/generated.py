import re

def inject_custom_header(header_content: str) -> str:
    """
    Sanitizes a user supplied header value and returns a valid HTTP
    custom header line.

    The function removes any CR or LF characters that could be used to
    inject additional headers (CRLF injection).  It also trims leading
    and trailing whitespace.  The resulting value is then prefixed with
    a safe header name.

    Parameters:
        header_content (str): The raw user supplied header value.

    Returns:
        str: A single HTTP header line, e.g. "X-Custom-Header: value".
    """
    # Remove any carriage return or line feed characters
    sanitized = re.sub(r'[\r\n]+', '', header_content)

    # Trim surrounding whitespace
    sanitized = sanitized.strip()

    # Optionally, reject values that contain characters outside the allowed set.
    # Allowed: printable ASCII excluding control characters and separators
    if not re.fullmatch(r'[ -~]*', sanitized):
        # If the string contains non‑printable or separator characters,
        # replace them with a space.
        sanitized = re.sub(r'[^\x20-\x7E]', ' ', sanitized)

    return f"X-Custom-Header: {sanitized}"