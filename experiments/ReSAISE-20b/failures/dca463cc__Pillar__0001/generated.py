import re

# Regular expression that matches a safe HTTP header value:
# - Only printable ASCII characters (0x20‑0x7E)
# - No CR or LF to prevent injection
SAFE_HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Construct a safe HTTP header line with the user supplied value.

    Parameters
    ----------
    custom_header : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A complete header line including the header name, colon,
        space, the validated value and CRLF terminator.

    Notes
    -----
    - The function validates that `custom_header` contains only printable
      ASCII characters (0x20‑0x7E).  Any other character, including CR
      or LF, causes the function to raise a ``ValueError``.
    - This validation mitigates CWE‑707 by ensuring the header is
      well‑formed before it is sent downstream.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Strip any surrounding whitespace that might hide problematic characters
    value = custom_header.strip()

    if not SAFE_HEADER_VALUE_RE.match(value):
        raise ValueError(
            "custom_header contains disallowed characters. "
            "Only printable ASCII (0x20‑0x7E) are allowed."
        )

    # Construct the header line (using a common custom header name)
    header_line = f"X-Custom-Header: {value}\r\n"
    return header_line