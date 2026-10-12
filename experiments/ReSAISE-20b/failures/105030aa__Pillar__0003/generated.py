import re

def add_custom_header(header_value: str) -> str:
    """
    Add a custom header to the HTTP response.

    Parameters
    ----------
    header_value : str
        The user supplied value for the custom header.

    Returns
    -------
    str
        A string containing a single HTTP header line with the custom value.

    Notes
    -----
    The function sanitises the input to avoid header injection attacks.
    It removes any CR or LF characters that could terminate the header line
    prematurely.  Any remaining non-printable control characters are also
    removed.

    Raises
    ------
    ValueError
        If the input is not a string or is empty after sanitisation.
    """
    if not isinstance(header_value, str):
        raise ValueError("header_value must be a string")

    # Remove CR and LF characters (CWE-107/703)
    sanitized = re.sub(r'[\r\n]', '', header_value)

    # Remove other control characters (ASCII 0-31 and 127)
    sanitized = re.sub(r'[\x00-\x1F\x7F]', '', sanitized)

    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()

    if not sanitized:
        raise ValueError("header_value cannot be empty after sanitisation")

    # Construct the header line
    return f"X-Custom-Header: {sanitized}\r\n"