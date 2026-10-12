import re

# Regular expression that matches a safe HTTP header value:
#   - Printable ASCII characters (space through tilde)
#   - No control characters, CR or LF to avoid header injection
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def append_user_header(user_header: str) -> str:
    """
    Append a custom header to the response output.

    The function validates that ``user_header`` contains only safe printable
    ASCII characters.  Any attempt to inject CR/LF or other control
    characters is rejected by raising ``ValueError``.  This protects against
    CWE-74 (HTTP Header Injection).

    Parameters:
        user_header (str): The custom header value supplied by the user.

    Returns:
        str: A complete HTTP header line including the custom header value,
             terminated by ``\\r\\n``.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    if not SAFE_HEADER_VALUE_RE.match(user_header):
        raise ValueError("Invalid header value: contains disallowed characters")

    # Construct the header line safely
    return f"X-Custom-Header: {user_header}\r\n"