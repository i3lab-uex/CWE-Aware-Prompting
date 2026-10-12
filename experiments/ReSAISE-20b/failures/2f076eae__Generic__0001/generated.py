import re

# Regular expression that matches a valid HTTP header field value.
# It disallows CR (`\r`) and LF (`\n`) characters which would break the header line.
HEADER_VALUE_RE = re.compile(r'^[^\r\n]*$')

def add_response_header(response_header: str) -> str:
    """
    Create a single HTTP header line from a user supplied value.

    Parameters
    ----------
    response_header : str
        The custom header value provided by the user.  It must not contain
        carriage‑return or line‑feed characters, as those would terminate the
        header and could be used for HTTP response splitting attacks.

    Returns
    -------
    str
        A fully formed header line, e.g. ``"X-Custom-Header: <value>"``.
        The header name is fixed to avoid ambiguity.

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    # Basic validation: ensure no CR or LF to prevent header injection
    if not HEADER_VALUE_RE.match(response_header):
        raise ValueError("Header value contains invalid characters (CR or LF).")

    # Construct the header line. The name is hard‑coded to avoid confusion.
    return f"X-Custom-Header: {response_header}"