import re

# Regex to match dangerous schemes at the beginning of a string.
# It allows optional leading whitespace and surrounding quotes.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""^\s*
        (?:['"]?)                     # optional leading quote
        (?P<scheme>                   # capture the scheme name
            javascript|vbscript       # currently flagged as dangerous
        )
        \s*:\s*                       # scheme separator
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regex to detect safe image data URLs.
_SAFE_DATA_URL_RE = re.compile(
    r"""^
        \s*['"]?                      # optional leading quote and whitespace
        data:
        image/
    """,
    re.IGNORECASE | re.VERBOSE,
)


def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the supplied string starts with a dangerous URL scheme
    (e.g., javascript:, vbscript:), excluding safe image-based data URLs.

    Parameters
    ----------
    input_url : str
        The string to be examined.

    Returns
    -------
    bool
        True if the input contains a dangerous scheme (excluding safe image data URLs),
        False otherwise.
    """
    if not isinstance(input_url, str):
        raise TypeError("input_url must be a string")

    # Quick bypass for safe image data URLs
    if _SAFE_DATA_URL_RE.match(input_url):
        return False

    # Check for dangerous schemes
    if _DANGEROUS_SCHEMES_RE.match(input_url):
        return True

    return False