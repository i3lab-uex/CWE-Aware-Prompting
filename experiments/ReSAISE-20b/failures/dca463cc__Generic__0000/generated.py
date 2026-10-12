import re

# Regular expression that matches a valid HTTP header value.
# According to RFC 7230, header field values may contain
# token characters and separators. This regex is a reasonable
# approximation that allows printable ASCII characters except
# control characters and the colon.
_HEADER_VALUE_RE = re.compile(r'^[!#$%&\'*+\-.^_`|~0-9a-zA-Z \t]+$')

def insert_custom_header(custom_header: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_header : str
        The value of the custom header supplied by the user.

    Returns
    -------
    str
        A full header line including the custom header name and value,
        e.g. ``"X-Custom-Header: <value>"``.

    Notes
    -----
    - The function validates that ``custom_header`` contains only
      characters allowed in HTTP header field values.
    - If the value does not match the regular expression, a
      ``ValueError`` is raised.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Strip leading/trailing whitespace to avoid accidental header injection.
    value = custom_header.strip()

    if not _HEADER_VALUE_RE.fullmatch(value):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII characters "
            "(excluding control chars and colon)"
        )

    # Construct the header line. Use a common custom header name.
    return f"X-Custom-Header: {value}"