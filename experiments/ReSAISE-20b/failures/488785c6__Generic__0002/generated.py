import re

# Regular expression to remove carriage return, line feed and other control characters
_CONTROL_CHARS_RE = re.compile(r'[\r\n\x00-\x1F\x7F]')

# Maximum allowed header value length (typical HTTP limits)
_MAX_HEADER_VALUE_LENGTH = 8192


def add_safe_header(custom_value: str) -> str:
    """
    Insert a user‑supplied value as a custom HTTP header while sanitizing it.

    The function removes any CR, LF or other control characters that could
    terminate the header line prematurely or enable injection attacks.
    It also ensures the value does not exceed a safe maximum length.

    Parameters
    ----------
    custom_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A header line of the form "X-Custom-Header: <sanitized_value>".

    Raises
    ------
    ValueError
        If the resulting header value would exceed the maximum length.
    """
    if not isinstance(custom_value, str):
        raise TypeError("custom_value must be a string")

    # Remove CR/LF and other control characters
    sanitized = _CONTROL_CHARS_RE.sub('', custom_value)

    # Truncate to the maximum allowed length
    if len(sanitized) > _MAX_HEADER_VALUE_LENGTH:
        raise ValueError(
            f"Header value too long: {len(sanitized)} bytes (max {_MAX_HEADER_VALUE_LENGTH})"
        )

    return f"X-Custom-Header: {sanitized}"