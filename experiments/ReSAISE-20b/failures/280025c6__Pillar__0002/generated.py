import re

# Regex pattern that matches only printable ASCII characters (0x20-0x7E)
# This excludes control characters, including CR (0x0D) and LF (0x0A),
# which are forbidden in HTTP header values to prevent injection attacks.
_HEADER_VALUE_PATTERN = re.compile(r'^[\x20-\x7E]*$')

def inject_custom_header(header_content: str) -> str:
    """
    Sanitize a user‑supplied header value and return it as part of an HTTP
    response header string.

    The function ensures that the header value contains only printable ASCII
    characters, thereby preventing CRLF injection and other header manipulation
    attacks (CWE‑707).

    Parameters:
        header_content (str): The raw user‑supplied header value.

    Returns:
        str: A sanitized header line, e.g. "X-Custom-Header: <value>".

    Raises:
        re.error: If the compiled regex pattern is invalid (unlikely in this
                  static context).
    """
    # Strip leading/trailing whitespace to avoid accidental spaces that could
    # interfere with header parsing.
    value = header_content.strip()

    if not _HEADER_VALUE_PATTERN.match(value):
        # If the input contains disallowed characters, replace them with a
        # safe placeholder or raise an error. Here we choose to truncate at the
        # first invalid character.
        match = _HEADER_VALUE_PATTERN.search(value)
        if match:
            value = value[:match.end()]
        else:
            # No valid portion; use an empty string to avoid injection.
            value = ''

    return f"X-Custom-Header: {value}"