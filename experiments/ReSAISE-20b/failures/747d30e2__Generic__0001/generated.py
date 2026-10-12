import re

# Regular expression that matches potentially dangerous URL schemes.
# It is case‑insensitive and allows optional whitespace before the scheme.
# The expression specifically excludes data URLs that start with
# "data:image/" (case‑insensitive), which are generally safe for images.
_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                               # optional leading whitespace
    (?:
        javascript: |                # plain JavaScript
        jscript:   |                # alternative spelling
        vbscript:  |                # VBScript
        data:\s*image/              # image data URLs (to be excluded)
    )
    ''',
    re.IGNORECASE | re.VERBOSE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if *s* contains a potentially malicious URL scheme
    (javascript:, jscript:, vbscript:) while ignoring image data URLs.
    
    Parameters
    ----------
    s : str
        The string to be examined for a malicious URL scheme.
    
    Returns
    -------
    bool
        True if *s* starts with a dangerous scheme (excluding image data URLs),
        otherwise False.
    """
    # We only care about the start of the string; any preceding text would
    # typically be handled by a parser that extracts the URL value.
    match = _DANGEROUS_SCHEME_RE.match(s)
    if not match:
        return False
    
    # If the matched group starts with "data:image/" we treat it as safe.
    if match.group(0).lower().startswith('data:image/'):
        return False
    
    # Otherwise it is a dangerous scheme.
    return True