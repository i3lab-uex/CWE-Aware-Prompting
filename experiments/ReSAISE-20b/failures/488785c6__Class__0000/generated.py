import re

def add_safe_header(custom_value: str) -> str:
    """
    Insert a user-supplied value as a custom HTTP header safely.

    The function sanitizes the input to prevent CRLF injection and
    ensures only printable US-ASCII characters (except colon) are used.
    It returns the complete header string ready to be added to an HTTP
    response.

    Args:
        custom_value (str): The user-provided header value.

    Returns:
        str: A sanitized HTTP header string, e.g. "X-Custom: value".
    """
    # Remove any carriage return or line feed characters
    sanitized = custom_value.replace("\r", "").replace("\n", "")

    # Allow only printable ASCII characters (0x20-0x7E) except colon
    sanitized = re.sub(r"[^\x20-\x7E]|:", "", sanitized)

    # Trim leading/trailing whitespace
    sanitized = sanitized.strip()

    return f"X-Custom: {sanitized}"