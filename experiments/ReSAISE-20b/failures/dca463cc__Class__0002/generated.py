import re

# Allowed characters for an HTTP header value: printable ASCII except CR and LF.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Safely construct an HTTP header line with a user supplied value.

    Parameters
    ----------
    custom_header : str
        The header value supplied by the user.  It must consist only of
        printable ASCII characters excluding CR (`\r`) and LF (`\n`).

    Returns
    -------
    str
        A header line in the form "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    if not isinstance(custom_header, str):
        raise ValueError("Header value must be a string")

    # Reject any CR or LF to prevent header injection (CWE-74).
    if not HEADER_VALUE_RE.fullmatch(custom_header):
        raise ValueError("Header value contains disallowed characters")

    # Construct the header line, appending CRLF as required by HTTP.
    return f"X-Custom-Header: {custom_header}\r\n"