import re

# Regex that matches a valid HTTP header value: any printable characters except CR and LF
_VALID_HEADER_VALUE_RE = re.compile(r"^[^\r\n]*$")


def add_custom_header(header_value: str) -> str:
    """
    Construct a custom HTTP header line with the supplied value.

    The function validates that the provided value does not contain
    carriage‑return or line‑feed characters, which would allow an attacker
    to inject additional headers or break the HTTP protocol.

    Parameters
    ----------
    header_value : str
        The user supplied value for the custom header.

    Returns
    -------
    str
        A single header line, terminated with CRLF.
    """
    if not isinstance(header_value, str):
        raise TypeError("header_value must be a string")

    # Validate that the value contains no CR or LF characters
    if not _VALID_HEADER_VALUE_RE.fullmatch(header_value):
        raise ValueError("header_value contains invalid characters (CR or LF)")

    # Construct the header line
    return f"X-Custom-Header: {header_value}\r\n"