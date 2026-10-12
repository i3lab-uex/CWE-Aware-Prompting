import re

# Regular expression that matches a valid HTTP header value.
# According to RFC 7230, header values may contain any CHAR except CTLs,
# but for safety we restrict to printable ASCII characters and allow
# optional whitespace at the ends.
HEADER_VALUE_RE = re.compile(r'^[\x20-\x7E]*$')

def insert_custom_header(custom_header: str) -> str:
    """
    Construct a safe HTTP header string from user input.

    Parameters
    ----------
    custom_header : str
        The value supplied by the user for the custom header.

    Returns
    -------
    str
        A well‑formed HTTP header line, e.g. "X-Custom-Header: value".

    Notes
    -----
    * The function validates that the header value contains only printable ASCII characters.
      This prevents injection of control characters or non‑ASCII data that could
      lead to header parsing issues or HTTP response splitting.
    * If the value fails validation, a ValueError is raised with a clear message
      rather than silently truncating or corrupting the header.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Strip leading/trailing whitespace to avoid header folding attacks.
    value = custom_header.strip()

    if not HEADER_VALUE_RE.match(value):
        raise ValueError(
            "Invalid header value: only printable ASCII characters are allowed"
        )

    # Construct the final header line. The header name is fixed to avoid
    # injection of additional headers via user input.
    return f"X-Custom-Header: {value}"