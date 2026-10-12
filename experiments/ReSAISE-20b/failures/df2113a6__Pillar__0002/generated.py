import re

# Regex pattern for a simple HTTP header value: allow printable ASCII except CR and LF
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(user_header: str) -> str:
    """
    Sanitize a user-supplied header value and return the full HTTP header line.

    Parameters
    ----------
    user_header : str
        The value supplied by the user for a custom header.

    Returns
    -------
    str
        A single HTTP header line in the form "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If the input contains characters that would break HTTP header structure.
    """
    # Remove any stray carriage return or line feed to prevent header injection
    sanitized = user_header.replace('\r', '').replace('\n', '')

    # Ensure the header value only contains allowed printable ASCII characters
    if not HEADER_VALUE_RE.match(sanitized):
        raise ValueError("Invalid header value: contains non-printable or disallowed characters")

    # Construct the final header line
    return f"X-Custom-Header: {sanitized}\r\n"