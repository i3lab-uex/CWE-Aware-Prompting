import re

# Regular expression to validate a safe HTTP header value.
# It must not contain CR (\\r) or LF (\\n) characters, which could
# lead to HTTP response splitting attacks.
_HEADER_VALUE_RE = re.compile(r"^[^\r\n]*$")

def add_response_header(response_header: str) -> str:
    """
    Construct a custom HTTP header line from the user supplied value.

    Parameters
    ----------
    response_header : str
        The header value provided by the user.  It must not contain CR or LF
        characters.

    Returns
    -------
    str
        A complete header line in the form ``X-Custom-Header: <value>\r\n``.

    Notes
    -----
    The function validates the input to avoid header injection attacks
    (CWE-7, CWE-707).  If the value contains disallowed characters the
    function raises a ValueError with an informative message.
    """
    if not isinstance(response_header, str):
        raise TypeError("response_header must be a string")

    # Ensure the header value is safe
    if not _HEADER_VALUE_RE.fullmatch(response_header):
        raise ValueError(
            "Invalid header value: must not contain CR or LF characters"
        )

    # Build the final header line
    return f"X-Custom-Header: {response_header}\r\n"