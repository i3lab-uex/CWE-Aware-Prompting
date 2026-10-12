import re

def add_safe_header(custom_value: str) -> str:
    """
    Construct a safe HTTP header string from user-supplied input.

    The function removes any carriage‑return or line‑feed characters and
    strips leading/trailing whitespace to prevent header injection.
    Only printable ASCII characters (except CR/LF) are allowed in the final
    value. Non‑printable control characters are removed.

    Parameters:
        custom_value (str): The user‑supplied header value.

    Returns:
        str: A complete header line, e.g.
             "X-Custom-Header: sanitized_value"
    """
    # Remove CR and LF to prevent injection of additional headers or
    # premature termination of the current header line.
    sanitized = re.sub(r'[\r\n]', '', custom_value)

    # Remove other control characters (0x00-0x1F, 0x7F)
    sanitized = re.sub(r'[\x00-\x1f\x7f]', '', sanitized)

    # Trim whitespace that might otherwise be interpreted as part of the
    # header value by downstream components.
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}"