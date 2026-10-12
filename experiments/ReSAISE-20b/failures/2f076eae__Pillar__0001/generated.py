import re

# Regular expression that matches a safe header value.
# It allows any printable ASCII characters except CR (\\r) and LF (\\n).
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def add_response_header(response_header: str) -> str:
    """
    Safely append a custom header to an HTTP response.

    Parameters
    ----------
    response_header : str
        The value for the custom header supplied by a user.

    Returns
    -------
    str
        A full HTTP header line including the custom value, e.g.
        "X-Custom-Header: <value>\r\n".

    Notes
    -----
    - The function guards against CRLF injection by ensuring the header value
      contains only printable ASCII characters and no line breaks.
    - The returned string is properly terminated with CRLF, suitable for
      concatenation into an HTTP response.

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Validate the header value
    if not SAFE_HEADER_VALUE_RE.match(response_header):
        raise ValueError(
            "Header value contains disallowed characters (CR, LF or non‑printable ASCII)"
        )

    # Construct the header line
    return f"X-Custom-Header: {response_header}\r\n"