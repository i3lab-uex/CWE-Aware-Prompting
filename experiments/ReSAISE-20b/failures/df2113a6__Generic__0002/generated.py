import re

def insert_custom_header(user_header: str) -> str:
    """
    Insert a custom header into an HTTP response string.

    The function sanitizes the user supplied header value to prevent
    injection of control characters such as CR and LF.  It then returns
    a header line in the form:
        X-Custom-Header: <sanitized value>

    Parameters
    ----------
    user_header : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A single header line with the sanitized value.

    Notes
    -----
    - Only CR (`\r`) and LF (`\n`) characters are removed.
      All other printable ASCII characters are allowed.  The function
      does not attempt to validate the value against RFC‑7230
      semantics beyond this basic sanitization.
    - If ``user_header`` is an empty string, the function returns
      a header with an empty value.
    """
    # Remove any carriage return or line feed characters to avoid
    # header injection attacks.
    sanitized = re.sub(r'[\r\n]+', '', user_header)

    # Construct the header line.  The header name is fixed to
    # "X-Custom-Header" to avoid user manipulation of the header name.
    return f"X-Custom-Header: {sanitized}"