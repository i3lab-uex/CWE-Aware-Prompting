import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response.

    Parameters
    ----------
    custom_value : str
        User‑supplied value for the custom header.

    Returns
    -------
    str
        A complete HTTP header line, e.g. "X-Custom-Header: value\r\n".

    Notes
    -----
    The function sanitises the input by removing any carriage‑return or line‑feed
    characters to prevent CRLF injection attacks.  It also validates that the
    argument is a string; otherwise a ``TypeError`` is raised.

    Raises
    ------
    TypeError
        If *custom_value* is not a string.
    re.error
        Propagated if the regular expression fails to compile (unlikely).
    """
    if not isinstance(custom_value, str):
        raise TypeError("custom_value must be a string")

    # Remove CR and LF characters to avoid header injection
    sanitized = re.sub(r'[\r\n]', '', custom_value)

    # Construct the header line (use a standard name; adjust as needed)
    return f"X-Custom-Header: {sanitized}\r\n"