import re

# RFC 7230 token characters: !#$%&'*+-.^_`|~0-9A-Za-z
_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")

def add_custom_header(header_value: str) -> str:
    """
    Return a header line with the user‑supplied value safely validated.

    Parameters
    ----------
    header_value : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A complete HTTP header line, e.g. "X-Custom-Header: foo\r\n".

    Raises
    ------
    ValueError
        If the header_value contains characters not allowed in a token.
    """
    if not isinstance(header_value, str):
        raise ValueError("Header value must be a string")

    # Validate against the token character set
    if not _TOKEN_RE.fullmatch(header_value):
        raise ValueError(
            "Invalid header value: contains disallowed characters "
            "(must be a token per RFC 7230)."
        )

    # Construct the header line (CRLF is required in HTTP headers)
    return f"X-Custom-Header: {header_value}\r\n"