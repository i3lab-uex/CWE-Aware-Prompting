import re

# Regular expression that matches potentially dangerous URL schemes.
# It ignores data URLs that start with 'data:image/' (case-insensitive).
_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^                           # start of string
    (?!data:image/[^;]*;)       # negative lookahead: reject data URLs with image mime type
    (?:                         # start of group for dangerous schemes
        javascript:|            # javascript scheme
        vbscript:|              # vbscript scheme
        lscript:|               # lscript (rare) scheme
        data:|                  # data scheme with non-image MIME types
        mailto:                 # mailto scheme (optional, can be considered dangerous)
    )
    ''',
    re.IGNORECASE | re.VERBOSE
)

def analyze_scheme(url: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme, aside from valid image data URLs;
        False otherwise.

    Notes
    -----
    The function uses a regular expression to detect the presence of dangerous schemes such as
    'javascript:', 'vbscript:', 'lscript:', or non-image data URLs.  Image data URLs are ignored
    because they are generally safe for embedding content.

    Examples
    --------
    >>> analyze_scheme('javascript:alert(1)')
    True
    >>> analyze_scheme('data:image/png;base64,...')
    False
    >>> analyze_scheme('data:text/html,<script>alert(1)</script>')
    True
    """
    if not isinstance(url, str):
        # If the input is not a string we cannot analyze it.
        return False

    # Strip leading whitespace to avoid false negatives caused by indentation or formatting
    url = url.lstrip()

    # If the regex finds a match, it means there's a dangerous scheme present.
    return bool(_DANGEROUS_SCHEME_RE.match(url))