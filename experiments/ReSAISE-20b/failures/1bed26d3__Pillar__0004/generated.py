import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme,
    excluding safe image-based data URLs.

    A dangerous scheme is any protocol followed by a colon at the start of
    the string (ignoring leading whitespace) that is **not** an image data URL.
    The check is case‑insensitive.

    Parameters
    ----------
    url_str : str
        The string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    # Pattern explanation:
    #   ^\s*          : optional leading whitespace at the start of the string
    #   (?!data:image/): negative lookahead to reject data URLs that are images
    #   [a-z][a-z0-9+\-.]* : a typical URL scheme (letters, digits, + . -)
    #   :              : the colon that terminates a scheme
    #
    # The re.IGNORECASE flag allows case‑insensitive matching.
    pattern = r'^\s*(?:(?!data:image/)[a-z][a-z0-9+\-.]*):'
    return re.match(pattern, url_str, flags=re.IGNORECASE) is not None