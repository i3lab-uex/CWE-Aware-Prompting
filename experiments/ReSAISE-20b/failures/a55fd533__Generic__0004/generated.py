import re

# Regular expression to match dangerous URL schemes.
# It matches any scheme that starts with the word "javascript", "vbscript",
# or any other common unsafe schemes, followed by a colon.
# It also ignores data URLs that start with "data:image/" (common for
# inline images). The regex is case‑insensitive and allows optional
# whitespace between the scheme name and the colon.
_DANGEROUS_SCHEMES_RE = re.compile(
    r"""
    (?<!data:image/)      # Negative lookbehind: not a data:image URL
    \b                    # Word boundary to avoid matching inside words
    (?:                   # Non‑capturing group for the scheme names
        javascript |
        vbscript |
        data:            # Exclude any other data: scheme (optional)
    )
    \s*:\s*               # Optional whitespace around the colon
    """,
    re.IGNORECASE | re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if *user_input* contains a dangerous URL scheme
    such as javascript: or vbscript:, ignoring valid image data URLs.
    
    Parameters
    ----------
    user_input : str
        The string to inspect for potentially malicious URL schemes.
    
    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    
    Notes
    -----
    The function uses a compiled regular expression for efficiency and
    is case‑insensitive. It ignores URLs that start with 'data:image/'
    because those are commonly used for inline images and are not
    typically malicious. Other 'data:' schemes are also ignored.
    
    Examples
    --------
    >>> contains_dangerous_scheme('javascript:alert(1)')
    True
    >>> contains_dangerous_scheme('vbscript:msgbox("test")')
    True
    >>> contains_dangerous_scheme('data:image/png;base64,iVBORw0KGgo...')
    False
    """
    if not isinstance(user_input, str):
        # Defensive: treat non‑string inputs as safe.
        return False

    # Search for any dangerous scheme in the input string
    return bool(_DANGEROUS_SCHEMES_RE.search(user_input))