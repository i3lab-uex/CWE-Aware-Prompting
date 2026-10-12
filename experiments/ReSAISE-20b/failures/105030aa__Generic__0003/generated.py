import re

# Regex pattern for a valid HTTP header field value (RFC 7230).
# This allows printable US-ASCII characters except control chars and
# the characters that are delimiters for header fields.
_HEADER_VALUE_PATTERN = re.compile(r'^[\x21-\x7E]+$')

def add_custom_header(header_value: str) -> str:
    """
    Construct an HTTP header line with a user supplied value.

    Parameters
    ----------
    header_value : str
        The custom header value provided by the user.  It must consist of
        printable US‑ASCII characters (0x21–0x7E).  Control characters and
        delimiters are disallowed to avoid injection attacks.

    Returns
    -------
    str
        A complete header line in the form:
            'X-Custom-Header: <header_value>\r\n'

    Raises
    ------
    ValueError
        If ``header_value`` does not match the allowed pattern.
    """
    if not isinstance(header_value, str):
        raise ValueError("header_value must be a string")

    # Validate the header value using the regex pattern.
    if not _HEADER_VALUE_PATTERN.fullmatch(header_value):
        raise ValueError(
            "Invalid header value: must contain only printable US-ASCII characters"
        )

    # Construct the header line.
    return f"X-Custom-Header: {header_value}\r\n"