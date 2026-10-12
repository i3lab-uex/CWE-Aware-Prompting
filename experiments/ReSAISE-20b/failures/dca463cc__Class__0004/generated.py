import re

# RFC 7230 token characters: !#$%&'*+-.^_`|~ plus alphanumerics
_TOKEN_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]+$")

def insert_custom_header(custom_header: str) -> str:
    """
    Construct a safe HTTP header string containing the user supplied
    custom_header value.

    Parameters:
        custom_header (str): The header value supplied by the user.

    Returns:
        str: A properly formatted header line, e.g.
             "Custom-Header: <value>\r\n".

    Raises:
        ValueError: If the supplied header value contains characters
                    that are not allowed in an HTTP token.
    """
    if not isinstance(custom_header, str):
        raise TypeError("custom_header must be a string")

    # Strip surrounding whitespace to avoid accidental injection
    value = custom_header.strip()

    # Validate against RFC 7230 token characters
    if not _TOKEN_RE.match(value):
        raise ValueError(
            "custom_header contains invalid characters for an HTTP header token"
        )

    # Build the header line
    return f"Custom-Header: {value}\r\n"