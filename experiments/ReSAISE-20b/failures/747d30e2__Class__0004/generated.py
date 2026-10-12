import re

# Regex that matches common malicious URL schemes.
# It looks for a scheme followed by ':' and ignores data URLs starting with "data:image".
# The pattern is case‑insensitive.
_MALICIOUS_SCHEME_RE = re.compile(
    r'''
    ^                           # start of string
    (?!data:image/[^;]*;)      # negative lookahead: not a data image URL
    (?:                        # start of scheme group
        javascript|
        jscript|
        vbscript|
        wscript|
        msxml|
        lscript|
        xsl|
        shell|
        vb
    )
    \s*:\s*                     # optional whitespace around colon
    ''',
    re.IGNORECASE | re.VERBOSE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if the input string starts with a potentially malicious URL scheme,
    excluding image data URLs. The function is case-insensitive and tolerant of
    whitespace around the colon.

    Parameters
    ----------
    s : str
        The string to test for a malicious scheme.

    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    """
    # Ensure we are dealing with a string; otherwise return False.
    if not isinstance(s, str):
        return False

    # Strip leading whitespace to avoid false negatives.
    s = s.lstrip()

    return bool(_MALICIOUS_SCHEME_RE.match(s))