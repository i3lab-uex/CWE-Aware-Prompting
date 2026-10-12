import re

# A simple whitelist of allowed header characters.
# RFC 7230 allows token and quoted-string. For safety we restrict to
# alphanumerics, spaces, dashes, underscores and dots.
_HEADER_VALUE_RE = re.compile(r'^[\w\s.-]+$')

def add_custom_header(header_value: str) -> str:
    """
    Create an HTTP header line with a user supplied value.

    The function validates the supplied value against a restrictive
    regular expression to mitigate CWE‑707 (Improper Neutralization).
    Only characters that are safe in an HTTP header value are allowed.
    If the value does not match, a ValueError is raised.

    Parameters
    ----------
    header_value : str
        The custom header value supplied by the user.

    Returns
    -------
    str
        A string representing a complete HTTP header line:
        "X-Custom-Header: <value>"

    Raises
    ------
    ValueError
        If the supplied header value contains disallowed characters.
    """
    if not isinstance(header_value, str):
        raise ValueError("header_value must be a string")

    if not _HEADER_VALUE_RE.match(header_value):
        raise ValueError(
            "header_value contains disallowed characters; "
            "only alphanumerics, spaces, dashes, underscores and dots are allowed"
        )

    return f"X-Custom-Header: {header_value}"