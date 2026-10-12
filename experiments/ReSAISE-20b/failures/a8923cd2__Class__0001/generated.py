import re

# Regular expression to remove any CR, LF or NUL characters that could break the header format
_SANITIZE_RE = re.compile(r'[\r\n\x00]')

def include_custom_header(custom_value: str) -> str:
    """
    Construct a safe HTTP header string with the user supplied value.

    Parameters
    ----------
    custom_value : str
        User supplied header value.  It must be a string; any embedded CR, LF or NUL
        characters are stripped to prevent header injection.

    Returns
    -------
    str
        The complete header line, e.g. "X-Custom-Header: <sanitized_value>\r\n".

    Notes
    -----
    The function does not raise any exceptions for normal usage.  If the input is
    not a string, ``TypeError`` will be raised by the assignment.  The regular
    expression may raise ``re.error`` only if it is incorrectly defined.
    """
    # Ensure we have a string (will raise TypeError otherwise)
    value = str(custom_value)

    # Strip dangerous characters that can terminate the header line
    sanitized = _SANITIZE_RE.sub('', value)

    # Strip leading/trailing whitespace to avoid accidental header splitting
    sanitized = sanitized.strip()

    # Construct the final header line
    return f"X-Custom-Header: {sanitized}\r\n"