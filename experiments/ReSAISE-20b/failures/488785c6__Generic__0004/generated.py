import re

# Pre‑compile a regex that removes any character outside the printable ASCII range,
# and also strips carriage return / line feed characters to prevent header injection.
_RE_INVALID_CHARS = re.compile(r'[\r\n]|[^\x20-\x7E]')

def add_safe_header(custom_value: str) -> str:
    """
    Insert a user‑supplied value as a custom header in the HTTP response.

    The function sanitizes `custom_value` by removing any control characters
    (CR, LF) and non‑printable ASCII bytes that could be used for header injection
    or other attacks. It then returns the full header string.

    Parameters
    ----------
    custom_value : str
        The user‑supplied header value.

    Returns
    -------
    str
        A string in the form "X-Custom-Header: <sanitized_value>".

    Notes
    -----
    * The function does not raise custom exceptions; any error in the regex
      compilation will surface as a `re.error`.
    * Empty or whitespace‑only values are trimmed to an empty string.
    """
    # Ensure the input is a string; coerce if necessary
    value = str(custom_value)

    # Strip leading/trailing whitespace to avoid accidental injection via spaces
    value = value.strip()

    # Remove disallowed characters (CR, LF, non‑printable ASCII)
    sanitized = _RE_INVALID_CHARS.sub('', value)

    # Construct the final header line
    return f'X-Custom-Header: {sanitized}'