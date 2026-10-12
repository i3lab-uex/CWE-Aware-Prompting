import re

# Regular expression to detect potentially malicious URL schemes.
# It matches any scheme that starts with a letter followed by
# alphanumeric characters, hyphens or dots, then a colon.
# We explicitly exclude data URLs that start with "data:image".
MALICIOUS_SCHEME_RE = re.compile(
    r'''
    ^\s*                                   # optional leading whitespace
    (?!data:image\b)                       # negative look‑ahead to skip image data URLs
    [a-z][a-z0-9\-\.]*\s*:                 # scheme (e.g., javascript:, vbscript:, jscript:)
    ''',
    re.IGNORECASE | re.VERBOSE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if the string starts with a potentially malicious URL scheme
    (e.g., javascript:, jscript:, vbscript:) and is not an image data URL.
    """
    if not isinstance(s, str):
        return False

    # Strip leading whitespace before checking
    s = s.lstrip()

    return bool(MALICIOUS_SCHEME_RE.match(s))