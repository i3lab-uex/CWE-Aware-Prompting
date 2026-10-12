import re

# Regex pattern that matches dangerous URL schemes while excluding valid image data URLs.
# The pattern is case‑insensitive and allows optional whitespace before the scheme.
_DANGEROUS_SCHEMES = re.compile(
    r"""
    ^\s*                                 # optional leading whitespace
    (?:
        javascript:|vbscript:|data:       # dangerous schemes or data URLs
    )
    (?!\s*image/[^;]*;)                  # negative look‑ahead to exclude image data URLs
    """,
    re.IGNORECASE | re.VERBOSE,
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether a string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_input : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful scheme (e.g. javascript:, vbscript:)
        and is not a valid image data URL; False otherwise.

    Notes
    -----
    The function uses a regular expression that:
      * Matches strings beginning with `javascript:` or `vbscript:`.
      * Also matches strings starting with `data:` but rejects those that contain an
        image MIME type (`image/...;`) to allow legitimate data URLs for images.
      * Is case‑insensitive and tolerates leading whitespace.

    Examples
    --------
    >>> verify_javascript_protocol('javascript:alert(1)')
    True
    >>> verify_javascript_protocol('vbscript:msgbox("x")')
    True
    >>> verify_javascript_protocol('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA')
    False
    >>> verify_javascript_protocol('data:text/html;base64,PGh0bWw+')
    True
    """
    if not isinstance(url_input, str):
        # Non‑string inputs are considered unsafe for the purpose of this check.
        return True

    match = _DANGEROUS_SCHEMES.match(url_input)
    return bool(match)