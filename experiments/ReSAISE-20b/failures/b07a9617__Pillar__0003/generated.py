import re

# Allowed characters in a header value: printable ASCII except control chars and CRLF.
# According to RFC 7230, a header value may contain any visible characters,
# but for safety we restrict to printable ASCII 0x20-0x7E, excluding CR (0x0D) and LF (0x0A).
# We also strip leading/trailing whitespace to avoid accidental injection.

HEADER_VALUE_REGEX = re.compile(r'^[\x20-\x7E]*$')

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a sanitized custom header into an HTTP response string.

    Parameters
    ----------
    custom_header_value : str
        The user-supplied value for the custom header.

    Returns
    -------
    str
        A complete HTTP header line with the sanitized value, e.g.
        "X-Custom-Header: <sanitized_value>\r\n".

    Raises
    ------
    re.error
        If the regex compilation fails (unlikely in normal operation).
    """
    # Normalize line endings: replace any CRLF or LF with a single space to avoid header injection.
    sanitized = custom_header_value.replace('\r', ' ').replace('\n', ' ')
    
    # Trim whitespace to avoid leading/trailing spaces that could be interpreted as part of the header.
    sanitized = sanitized.strip()
    
    # Enforce allowed character set. If any disallowed char is present, replace it with a space.
    # This ensures the header remains well-formed and mitigates injection attacks.
    if not HEADER_VALUE_REGEX.match(sanitized):
        sanitized = ''.join(
            ch if 0x20 <= ord(ch) <= 0x7E and ch not in '\r\n' else ' '
            for ch in sanitized
        )
    
    # Construct the final header line with CRLF termination.
    return f"X-Custom-Header: {sanitized}\r\n"