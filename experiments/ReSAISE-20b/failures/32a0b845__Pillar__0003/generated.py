import re

def add_customized_header(header_content: str) -> str:
    """
    Create a safe HTTP header line with the user supplied value.

    The function sanitizes the input to prevent CRLF injection and
    ensures that only printable ASCII characters are included in the
    header value.  The resulting string is a complete header line,
    including the field name and terminating CRLF.

    Parameters
    ----------
    header_content : str
        The user supplied value for the custom header.

    Returns
    -------
    str
        A single HTTP header line: "X-Custom-Header: <sanitized value>\r\n"

    Raises
    ------
    re.error
        If the regular expression compilation fails.
    """
    # Remove any CR or LF characters to prevent header injection
    sanitized = re.sub(r'[\r\n]+', '', header_content)

    # Allow only printable ASCII characters (0x20-0x7E) for safety
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # Trim leading/trailing whitespace
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}\r\n"