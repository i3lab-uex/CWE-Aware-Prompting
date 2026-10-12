import re

# Regular expression to validate an HTTP header value.
# It allows printable ASCII characters except CR and LF.
_HEADER_VALUE_RE = re.compile(r"^[\x20-\x7E]+$")

def add_response_header(response_header: str) -> str:
    """
    Return a complete HTTP header line that includes the user supplied
    `response_header` value. The function sanitises the input to avoid
    CR/LF injection (CWE‑74).

    Parameters
    ----------
    response_header : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A string in the form "X-Custom-Header: <sanitised value>".

    Raises
    ------
    ValueError
        If the supplied header contains disallowed characters.
    """
    # Ensure the input is a string
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Strip surrounding whitespace but keep internal spaces
    header_value = response_header.strip()

    # Validate the header value using a strict regular expression.
    if not _HEADER_VALUE_RE.fullmatch(header_value):
        raise ValueError(
            "Header value contains disallowed characters (only printable ASCII "
            "characters are allowed, no CR or LF)"
        )

    # Construct the final header line
    return f"X-Custom-Header: {header_value}"