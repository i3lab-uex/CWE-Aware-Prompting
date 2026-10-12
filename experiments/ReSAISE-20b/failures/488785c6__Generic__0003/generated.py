import re

# Regular expression that matches any characters that are not allowed in HTTP header values.
# RFC 7230 specifies that header field-values may contain any visible ASCII characters
# (0x20–0x7E) except for CR (0x0D) and LF (0x0A).  We also disallow the
# horizontal tab (0x09) because it can be used for header folding.
INVALID_HEADER_CHARS = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]+')

def add_safe_header(custom_value: str) -> str:
    """
    Return a safe HTTP header string that includes the user supplied value.

    The function removes any characters that would break the HTTP protocol
    (CR, LF, control characters) and ensures the header line ends with a CRLF.
    The returned string can be safely concatenated to an HTTP response.

    Parameters
    ----------
    custom_value : str
        User supplied header value.

    Returns
    -------
    str
        The full header line, e.g. "X-Custom-Header: <sanitized_value>\r\n".

    Raises
    ------
    re.error
        If the regex compilation fails (unlikely in this static context).
    """
    # Sanitize by stripping disallowed characters.
    sanitized = INVALID_HEADER_CHARS.sub('', custom_value)

    # Collapse any remaining whitespace to a single space to avoid accidental
    # folding or long lines that might be misinterpreted.
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # Build the final header line.
    return f"X-Custom-Header: {sanitized}\r\n"