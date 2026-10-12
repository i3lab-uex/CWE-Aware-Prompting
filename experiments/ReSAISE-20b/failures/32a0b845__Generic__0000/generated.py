import re

# Allowed characters: printable ASCII excluding control chars and CRLF.
_HEADER_SANITIZE_RE = re.compile(r'[\r\n]+')

def add_customized_header(header_content: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    The function sanitizes the user-provided `header_content` by removing any
    carriage return or line feed characters to prevent header injection.
    The resulting header is returned as a single line string.

    Parameters
    ----------
    header_content : str
        The user-defined value for the custom header.

    Returns
    -------
    str
        A string representing a single HTTP header line:
        "X-Custom-Header: <sanitized_value>"

    Raises
    ------
    re.error
        If the regular expression used for sanitization fails (unlikely).
    """
    # Remove any CR or LF characters to avoid injection.
    sanitized = _HEADER_SANITIZE_RE.sub('', header_content)

    # Optionally, collapse multiple spaces into one.
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()

    # Build the header line.
    return f"X-Custom-Header: {sanitized}"