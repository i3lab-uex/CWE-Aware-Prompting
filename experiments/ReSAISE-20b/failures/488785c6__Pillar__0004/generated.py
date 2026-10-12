import re

# Regular expression to match any carriage return, line feed or other control characters.
CONTROL_CHARS_RE = re.compile(r'[\r\n\x00-\x1f\x7f]+')

# Regular expression to match any non‑ASCII printable characters.
NON_PRINTABLE_RE = re.compile(r'[^\x20-\x7e]')

def add_safe_header(custom_value: str) -> str:
    """
    Return an HTTP header string containing a user supplied value,
    after sanitizing it to prevent header injection and other
    security issues.

    Parameters
    ----------
    custom_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A header line in the form "X-Custom-Header: <sanitized_value>"
    """
    # 1. Remove any CR, LF or other control characters that could break
    # the header format.
    sanitized = CONTROL_CHARS_RE.sub('', custom_value)

    # 2. Remove any non‑ASCII printable characters to keep the header
    # well‑formed and avoid encoding issues.
    sanitized = NON_PRINTABLE_RE.sub('', sanitized)

    # 3. Strip leading/trailing whitespace to avoid accidental
    # injection via spaces.
    sanitized = sanitized.strip()

    # 4. Ensure the value is not empty; if it is, use a safe default.
    if not sanitized:
        sanitized = 'default'

    return f'X-Custom-Header: {sanitized}'