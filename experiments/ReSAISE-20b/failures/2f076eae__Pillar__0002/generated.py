import re

# Regular expression that matches a safe header value:
# - No carriage return or line feed (CRLF)
# - Only printable ASCII characters
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def add_response_header(response_header: str) -> str:
    """
    Build a single HTTP header line from a user supplied value.

    The function validates the input to guard against CRLF injection
    and other control characters that could break the header format.
    The returned string is a complete header line ready to be added
    to an HTTP response, e.g.:

        "X-User-Custom: my-value\r\n"

    Parameters
    ----------
    response_header : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A fully formed HTTP header line containing the custom value.
    """
    if not isinstance(response_header, str):
        raise TypeError("response_header must be a string")

    # Strip surrounding whitespace to avoid accidental injection
    value = response_header.strip()

    # Ensure the value does not contain CR or LF characters.
    if not HEADER_VALUE_RE.match(value):
        raise ValueError("Invalid header value: contains control characters")

    # Construct the header line. The header name is fixed to avoid
    # manipulation of the header field itself.
    header_line = f"X-User-Custom: {value}\r\n"
    return header_line