import re

# RFC 7230 token characters (excluding CTLs and separators)
_TOKEN_RE = re.compile(r'^[!#$%&\'*+\-.^_`|~0-9a-zA-Z]+$')

def add_response_header(response_header: str) -> str:
    """
    Construct a safe HTTP header line using the user supplied value.

    Parameters
    ----------
    response_header : str
        The custom header value provided by the user.

    Returns
    -------
    str
        A fully formed header line: "Custom-Header: <value>\r\n".

    Notes
    -----
    - The function validates that the header value consists only of
      token characters defined by RFC 7230. This prevents CRLF injection
      and other header injection attacks (CWE‑74).
    - If the value does not match the pattern, a ValueError is raised.
    """
    if not isinstance(response_header, str):
        raise TypeError("response_header must be a string")

    # Strip leading/trailing whitespace (not allowed in token)
    value = response_header.strip()

    if not _TOKEN_RE.match(value):
        raise ValueError(
            "Invalid header value: only token characters (alphanumerics and "
            "!#$%&'*+-.^_`|~) are allowed"
        )

    return f"Custom-Header: {value}\r\n"