import re

def add_custom_header(header_value: str) -> str:
    """
    Add a custom header to the HTTP response.

    Parameters
    ----------
    header_value : str
        The user supplied value for the custom header.  It must match the
        RFC‑7230 token syntax (alphanumerics and a limited set of
        punctuation).  Any value that does not match will raise a ValueError.

    Returns
    -------
    str
        The header line, including the trailing CRLF sequence.

    Notes
    -----
    * The function uses a regular expression that follows the RFC‑7230
      definition of a token: one or more characters from the set
      ``!#$%&'*+-.^_`|~`` and alphanumerics.
    * This validation prevents header injection attacks where a user could
      inject CRLF characters to break out of the header context.
    """
    # RFC‑7230 token pattern (simplified, but safe for most use cases)
    TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")

    if not isinstance(header_value, str):
        raise TypeError("header_value must be a string")

    if not TOKEN_RE.fullmatch(header_value):
        raise ValueError(
            "header_value contains invalid characters; "
            "only RFC‑7230 token characters are allowed"
        )

    # Construct the header line with CRLF termination
    return f"X-Custom-Header: {header_value}\r\n"