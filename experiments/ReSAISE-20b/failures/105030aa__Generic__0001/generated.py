import re

# Regular expression that matches a safe header value:
# - no carriage return or line feed (CRLF)
# - no control characters except horizontal tab
SAFE_HEADER_VALUE_RE = re.compile(r'^[^\r\n\x00-\x08\x0B\x0C\x0E-\x1F]*$')

def add_custom_header(header_value: str) -> str:
    """
    Construct a custom HTTP header line using the supplied value.

    Parameters
    ----------
    header_value : str
        The custom header value provided by the user.

    Returns
    -------
    str
        A complete HTTP header line in the form:
            "X-Custom-Header: <header_value>\r\n"

    Raises
    ------
    ValueError
        If the supplied header value contains prohibited characters such as CRLF,
        control characters, or other characters that would break HTTP header syntax.
    """
    if not isinstance(header_value, str):
        raise ValueError("header_value must be a string")

    # Ensure the value does not contain any forbidden characters
    if not SAFE_HEADER_VALUE_RE.match(header_value):
        raise ValueError("header_value contains invalid characters")

    # Construct the header line
    return f"X-Custom-Header: {header_value}\r\n"