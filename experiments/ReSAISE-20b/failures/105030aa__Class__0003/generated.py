import re

def add_custom_header(header_value: str) -> str:
    """
    Construct a safe custom HTTP header line.

    The function removes any characters that could terminate the header
    or inject additional headers (CR, LF) and strips non‑printable control
    characters.  The resulting header is of the form:

        X-Custom-Header: <sanitized_value>\r\n

    Parameters
    ----------
    header_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A single header line ready to be appended to an HTTP response.

    Notes
    -----
    - CR (`\r`) and LF (`\n`) are removed to prevent header injection.
    - Control characters (ASCII < 32) except tab (`\t`) are stripped to
      maintain header integrity.
    - The function does not raise exceptions for normal usage; only a
      malformed regex would cause an `re.error`.
    """
    # Remove carriage returns and line feeds that could terminate the header
    sanitized = re.sub(r'[\r\n]', '', header_value)

    # Remove other control characters (except tab) to avoid malformed headers
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', sanitized)

    # Trim leading/trailing whitespace to keep header tidy
    sanitized = sanitized.strip()

    return f"X-Custom-Header: {sanitized}\r\n"