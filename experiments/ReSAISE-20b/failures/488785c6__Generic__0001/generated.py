import re

# Pre‑compiled regex to strip disallowed characters:
#   - control characters (0x00–0x1F and 0x7F)
#   - CRLF sequences used for header injection
DISALLOWED_PATTERN = re.compile(r'[\x00-\x1F\x7F]|(\r|\n)')

# Optional: limit header length to avoid excessive payloads
MAX_HEADER_LENGTH = 200

def add_safe_header(custom_value: str) -> str:
    """
    Sanitize a user‑supplied string and return an HTTP header line
    that safely includes the value.

    Parameters:
        custom_value (str): The raw header value supplied by a user.

    Returns:
        str: A properly formatted HTTP header line,
             e.g. "X-Custom-Header: sanitized_value".

    Raises:
        re.error: If the regex pattern fails to compile (unlikely).
    """
    if not isinstance(custom_value, str):
        # Coerce non‑string input to string; this mirrors typical
        # web frameworks that accept any type.
        custom_value = str(custom_value)

    # Remove control characters and CRLF sequences
    sanitized = DISALLOWED_PATTERN.sub('', custom_value)

    # Trim to a reasonable length to avoid excessively long headers
    if len(sanitized) > MAX_HEADER_LENGTH:
        sanitized = sanitized[:MAX_HEADER_LENGTH]

    # Build the header line
    return f"X-Custom-Header: {sanitized}"