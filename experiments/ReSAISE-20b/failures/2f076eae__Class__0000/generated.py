import re

# Regular expression that matches a valid HTTP token (RFC 7230, section 3.2.6)
# Tokens consist of any VCHAR except delimiters and whitespace.
TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9a-zA-Z]+$")

# Regular expression that matches a quoted-string without embedded CR or LF
QUOTED_STRING_RE = re.compile(r'^"[^"\r\n]*"$')

def add_response_header(response_header: str) -> str:
    """
    Construct a custom HTTP header line safely.

    Parameters
    ----------
    response_header : str
        The user‑supplied value for the custom header.  It must be a valid
        HTTP token or quoted‑string that does not contain CR (`\r`) or LF (`\n`).

    Returns
    -------
    str
        A complete header line of the form ``X-Custom-Header: <value>\r\n``.

    Notes
    -----
    * The function sanitises the input to prevent CRLF injection (CWE‑74).
    * If ``response_header`` does not match either the token or quoted-string
      pattern, a :class:`ValueError` is raised.

    Raises
    ------
    ValueError
        If the supplied header value contains characters that would break
        HTTP parsing or could be used for injection.
    """
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Reject CR or LF outright
    if "\r" in response_header or "\n" in response_header:
        raise ValueError("Header value cannot contain CR or LF characters")

    # Validate against token or quoted-string
    if not (TOKEN_RE.match(response_header) or QUOTED_STRING_RE.match(response_header)):
        raise ValueError("Header value contains invalid characters")

    # Construct the header line safely
    return f"X-Custom-Header: {response_header}\r\n"