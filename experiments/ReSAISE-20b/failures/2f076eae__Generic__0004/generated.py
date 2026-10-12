import re

# Regular expression for a simple HTTP header value:
#   - printable ASCII characters (0x21-0x7E)
#   - excluding colon ':' and CR/LF to avoid header injection.
HEADER_VALUE_RE = re.compile(r'^[\x21-\x7E]+$')

def add_response_header(response_header: str) -> str:
    """
    Return a full HTTP header string with the supplied custom value.

    Parameters
    ----------
    response_header : str
        The user‑supplied header value.  It must consist solely of printable
        ASCII characters (0x21‑0x7E) and cannot contain a colon or CR/LF
        characters.  This simple validation protects against header injection.

    Returns
    -------
    str
        A string in the form ``"Custom-Header: <value>"``.

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Strip surrounding whitespace to avoid accidental injection.
    cleaned = response_header.strip()

    if not HEADER_VALUE_RE.match(cleaned):
        raise ValueError(
            "Invalid header value: must contain only printable ASCII "
            "(0x21-0x7E) and cannot include ':' or CR/LF characters"
        )

    return f"Custom-Header: {cleaned}"