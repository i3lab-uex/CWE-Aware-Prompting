import re

# Regular expression that matches dangerous URL schemes.
# It ignores case, allows optional whitespace before the colon,
# and excludes valid image data URLs (data:image/...).
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    (?i)                               # case-insensitive
    (?:                                # non-capturing group for the scheme part
        javascript:                    # "javascript:" scheme
      | vbscript:                      # "vbscript:" scheme
      | data\s*:\s*                    # start of a data URI
        (?!image)                      # but not an image
    )
    """,
    re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if the input string contains a potentially dangerous URL
    scheme (e.g. javascript:, vbscript:) but ignore safe image data URLs.

    Parameters
    ----------
    user_input : str
        The string to inspect for malicious URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # Quick sanity check: empty input cannot contain a dangerous scheme
    if not user_input:
        return False

    # Search for the pattern anywhere in the input string.
    return bool(_DANGEROUS_SCHEMES_RE.search(user_input))