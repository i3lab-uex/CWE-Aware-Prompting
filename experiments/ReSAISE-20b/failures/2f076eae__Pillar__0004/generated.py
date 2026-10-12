import re

# Regular expression for a valid HTTP token (RFC 7230 Section 3.2.6)
TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-zA-Z]+$")

# Regular expression to detect CR or LF characters in header values
CRLF_RE = re.compile(r"[\r\n]")

def add_response_header(response_header: str) -> str:
    """
    Construct a custom HTTP header line with the provided value.

    The function validates that the header name and value are safe
    for inclusion in an HTTP response.  The header name is fixed to
    'X-Custom-Header' (a common convention for user-defined headers).

    Parameters:
        response_header: str
            The value supplied by the user for the custom header.

    Returns:
        str
            A complete header line suitable for inclusion in an HTTP
            response, e.g. "X-Custom-Header: myvalue".

    Raises:
        ValueError
            If the supplied value contains prohibited characters or
            is otherwise not a valid header value.
    """
    # Ensure the value does not contain CR or LF characters
    if CRLF_RE.search(response_header):
        raise ValueError("Header value contains prohibited CR or LF characters")

    # Optionally, enforce a maximum length (e.g., 255 bytes)
    if len(response_header.encode('utf-8')) > 255:
        raise ValueError("Header value exceeds maximum allowed length")

    # Validate that the value consists of safe token characters
    if not TOKEN_RE.match(response_header):
        raise ValueError("Header value contains invalid token characters")

    # Construct the header line
    return f"X-Custom-Header: {response_header}"