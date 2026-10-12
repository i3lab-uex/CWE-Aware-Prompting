import re

# Regex pattern for a valid HTTP header field value.
# RFC 7230 allows any CHAR except CTLs and the delimiter `:` and CRLF.
# For simplicity we disallow CR, LF, colon, and leading/trailing whitespace.
_HEADER_VALUE_RE = re.compile(r'^[^\r\n:]+$')

def add_custom_header(header_value: str) -> str:
    """
    Construct an HTTP header line with the supplied custom header value.

    Parameters
    ----------
    header_value : str
        The custom header value provided by the user. It must not contain CR, LF,
        or a colon.

    Returns
    -------
    str
        A header line in the form ``X-Custom-Header: <value>\r\n``.

    Raises
    ------
    ValueError
        If `header_value` contains characters that are not allowed in an HTTP
        header field value.
    """
    if not isinstance(header_value, str):
        raise TypeError("header_value must be a string")

    if not _HEADER_VALUE_RE.match(header_value):
        raise ValueError(
            "header_value contains invalid characters (CR, LF, or ':')"
        )

    return f"X-Custom-Header: {header_value}\r\n"