import re

# Regular expression that matches potentially malicious URL schemes.
# It looks for the scheme at the beginning of a string or after whitespace, followed by ':'.
MALICIOUS_SCHEME_RE = re.compile(
    r"""(?i)                    # case-insensitive
        (?<![^\s])               # start of string or whitespace
        (javascript|jscript|vbscript)   # forbidden schemes
        \s*:\s*                  # optional whitespace around ':'
    """,
    re.VERBOSE,
)

# Regular expression that matches image data URLs.
DATA_IMAGE_RE = re.compile(
    r"""(?i)                    # case-insensitive
        data\s*:\s*
        image\/                 # MIME type starts with 'image/'
    """,
    re.VERBOSE,
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if the string contains a potentially malicious URL scheme
    (javascript:, jscript:, vbscript:), but False if it is an image data URL.
    """
    if not isinstance(s, str):
        # Non-string input is considered safe
        return False

    # First check for image data URLs – these are allowed.
    if DATA_IMAGE_RE.search(s):
        return False

    # If any malicious scheme is found, flag it.
    return bool(MALICIOUS_SCHEME_RE.search(s))