import re

# Regular expression that matches a valid HTTP header value.
# Allowed characters: letters, digits, whitespace, hyphen and underscore.
_HEADER_VALUE_RE = re.compile(r'^[\w\s-]+$')


def add_response_header(response_header: str) -> str:
    """
    Return a string containing the full HTTP header line for a custom
    response header. The value is validated against a simple whitelist of
    characters to mitigate injection attacks.

    Parameters
    ----------
    response_header : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A string formatted as "Custom-Header: <value>".

    Raises
    ------
    ValueError
        If ``response_header`` contains characters that are not allowed.
    """
    if not isinstance(response_header, str):
        raise ValueError("Header value must be a string")

    # Strip leading/trailing whitespace before validation
    cleaned = response_header.strip()

    if not _HEADER_VALUE_RE.fullmatch(cleaned):
        raise ValueError(
            "Header value contains invalid characters; "
            "only letters, digits, spaces, hyphens and underscores are allowed"
        )

    return f"Custom-Header: {cleaned}"