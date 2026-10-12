import re

# Allowed characters for a header value:
# RFC 7230 allows any VCHAR or obs-text, but we restrict to printable
# characters excluding CR (\\r) and LF (\\n) to prevent injection.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7e]*$')  # printable ASCII only

def append_user_header(user_header: str) -> str:
    """
    Return a properly formatted HTTP header line containing the user-specified
    value. The function sanitises the input to prevent CRLF injection (CWE-74).

    Parameters
    ----------
    user_header : str
        The header value supplied by the user.

    Returns
    -------
    str
        A complete header string, e.g. 'X-Custom-Header: <sanitised_value>'

    Notes
    -----
    * The function rejects any input containing carriage return (\\r) or line feed
      (\\n) characters, which could otherwise break the header structure.
    * Only printable ASCII characters are accepted.  If other Unicode
      characters are required, adjust the regular expression accordingly.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Reject empty header values – you can change this behaviour if needed
    if user_header == "":
        raise ValueError("user_header cannot be empty")

    # Ensure no CR or LF characters are present
    if "\r" in user_header or "\n" in user_header:
        raise ValueError("Header value must not contain CR or LF characters")

    # Validate against the allowed character set
    if not HEADER_VALUE_RE.fullmatch(user_header):
        raise ValueError("Header value contains disallowed characters")

    # Construct the header line
    return f"X-Custom-Header: {user_header}"