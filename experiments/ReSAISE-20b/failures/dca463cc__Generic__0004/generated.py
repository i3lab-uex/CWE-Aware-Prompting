import re

# Regular expression to validate a header value:
# - Must not contain CR (\r) or LF (\n)
# - Must be printable ASCII (0x20-0x7E) or tab
HEADER_VALUE_RE = re.compile(r'^[\t\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_header : str
        The value to use for the header.  It must be a valid HTTP header
        value: no carriage‑return or line‑feed characters, and only
        printable ASCII (0x20–0x7E) or tab.

    Returns
    -------
    str
        The full header line, including the header name and CRLF terminator.

    Raises
    ------
    ValueError
        If the header value contains disallowed characters.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Validate the header value
    if not HEADER_VALUE_RE.match(custom_header):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII characters "
            "(no CR or LF)."
        )

    # Construct the header line.  The header name is hard‑coded to
    # "X-Custom-Header" for this example.  Adjust as needed.
    header_line = f"X-Custom-Header: {custom_header}\r\n"
    return header_line