import re

# Regular expression to match dangerous URL schemes.
# The pattern looks for the beginning of a string (optionally preceded by whitespace)
# followed by a scheme name and a colon.  It excludes valid image data URLs
# (`data:image/...`) by ensuring that if the scheme is `data:` it must not be
# followed immediately by `image/`.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""^\s*                                 # optional leading whitespace
        (?:                                   # start non-capturing group for scheme
            (?P<scheme>javascript|vbscript)   # javascript or vbscript schemes
            |                                 # OR
            data:(?!image/)                   # data: scheme not followed by image/
        )
    """,
    re.IGNORECASE | re.VERBOSE
)

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects whether a given string contains a dangerous URL scheme.

    Parameters
    ----------
    url_string : str
        The input string to inspect for potentially malicious URL schemes.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme (javascript:, vbscript:,
        or data: not followed by image/), False otherwise.

    Notes
    -----
    - The function is case-insensitive.
    - Leading whitespace is ignored.
    - Only the scheme part at the start of the string is considered; any
      subsequent characters are irrelevant for this check.
    """
    if not isinstance(url_string, str):
        raise TypeError("url_string must be a string")

    # Attempt to match the dangerous scheme at the beginning of the string.
    return bool(_DANGEROUS_SCHEMES_RE.match(url_string))