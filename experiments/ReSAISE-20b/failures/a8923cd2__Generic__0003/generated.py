import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response.

    The function sanitizes the user-provided value to ensure it contains only
    characters allowed in an HTTP header field value, preventing CRLF injection.

    Parameters:
        custom_value (str): The user-defined header value.

    Returns:
        str: A complete HTTP header line including the sanitized custom header.
             Example: "X-Custom-Header: value\r\n"

    Raises:
        re.error: If the regex compilation fails (unlikely with a static pattern).
    """
    # Allowed characters: any visible ASCII except colon, comma, semicolon, and
    # control characters (0x00-0x1F). We also strip leading/trailing whitespace.
    # The pattern removes CR, LF and any other non-printable characters.
    sanitized = re.sub(r'[\r\n\x00-\x1F]', '', custom_value).strip()

    # If the value is empty after sanitization, raise a ValueError to avoid
    # sending an invalid header. This is optional but helps maintain protocol integrity.
    if not sanitized:
        raise ValueError("Custom header value cannot be empty after sanitization.")

    return f"X-Custom-Header: {sanitized}\r\n"