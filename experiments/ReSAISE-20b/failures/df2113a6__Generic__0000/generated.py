import re

# Regular expression to validate an HTTP header field value.
# It allows printable ASCII characters except CR, LF and control characters.
HEADER_VALUE_RE = re.compile(r"^[^\x00-\x1F\x7F\r\n]+$")


def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into the response headers.

    The function sanitizes `user_header` to ensure it does not contain
    characters that could break the HTTP header format (e.g. CR or LF).
    The sanitized value is then returned as a complete header line.

    Parameters
    ----------
    user_header : str
        The value supplied by the user for the custom header.

    Returns
    -------
    str
        A full HTTP header line in the form:
            "Custom-Header: <sanitized_value>\r\n"

    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely in this context).
    ValueError
        If `user_header` contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Strip leading/trailing whitespace but preserve internal spaces
    header_value = user_header.strip()

    if not HEADER_VALUE_RE.match(header_value):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII "
            "characters and cannot include CR or LF."
        )

    return f"Custom-Header: {header_value}\r\n"