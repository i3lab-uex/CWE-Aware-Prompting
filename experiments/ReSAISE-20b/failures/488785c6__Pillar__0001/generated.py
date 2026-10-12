import re

# Regular expression to allow printable ASCII characters except CR, LF and control codes.
# This pattern matches any string that does NOT contain:
#   - Carriage Return (CR, \r)
#   - Line Feed (LF, \n)
#   - Control characters 0x00-0x1F
#   - Delete character (0x7F)
_HEADER_VALUE_RE = re.compile(r'^[^\r\n\x00-\x1F\x7F]+$')


def add_safe_header(custom_value: str) -> str:
    """
    Return a well‑formed HTTP header string containing the user supplied
    custom value after validating it against the header rules.

    The function accepts only values that do not contain CR, LF or any
    control characters.  If the value fails validation it is stripped of
    those characters and any leading/trailing whitespace.

    Parameters
    ----------
    custom_value : str
        The user supplied header value.

    Returns
    -------
    str
        A complete HTTP header string of the form:
            "X-Custom-Header: <sanitized_value>"
    """
    # Strip leading/trailing whitespace to avoid accidental injection.
    value = custom_value.strip()

    if not _HEADER_VALUE_RE.match(value):
        # Remove problematic characters while preserving printable content.
        # We replace CR, LF and control codes with a single space.
        value = re.sub(r'[\r\n\x00-\x1F\x7F]+', ' ', value).strip()

    # Construct the header line.  The colon and a single space are part of
    # the HTTP header syntax.
    return f"X-Custom-Header: {value}"