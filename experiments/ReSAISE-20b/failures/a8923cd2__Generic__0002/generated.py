import re

# Regular expression for a safe HTTP header value.
# Allows token characters or a quoted string with escaped quotes and backslashes.
_SAFE_HEADER_VALUE_RE = re.compile(
    r'^(?:[!#$%&\'*+\-.^_`|~0-9a-zA-Z]+|'          # token
    r'"(?:\\["\\]|[^"\r\n])*" )$'                 # quoted-string
)

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_value : str
        User supplied value for the custom header. It must match the safe
        pattern defined by _SAFE_HEADER_VALUE_RE.

    Returns
    -------
    str
        The full header line including the CRLF terminator.
        Example: "X-Custom-Header: myValue\r\n"

    Raises
    ------
    ValueError
        If the custom_value does not conform to a safe HTTP header value.
    """
    if not isinstance(custom_value, str):
        raise ValueError("custom_value must be a string")

    # Validate the value against the allowed pattern
    if not _SAFE_HEADER_VALUE_RE.match(custom_value):
        raise ValueError("custom_value contains unsafe characters for HTTP headers")

    # Construct the header line
    return f"X-Custom-Header: {custom_value}\r\n"