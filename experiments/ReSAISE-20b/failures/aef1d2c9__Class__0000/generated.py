import re

# Regular expression to detect dangerous URL schemes.
# It matches strings that start with a scheme followed by ':' and
# are NOT a data URI for an image (data:image/...).
#
# The pattern works as follows:
#   1. ^\s*          – optional leading whitespace.
#   2. (?:[^:]+)     – capture any scheme characters up to the first ':'.
#   3. :             – literal colon separating scheme from rest of URL.
#   4. (?!\s*data:image) – negative look‑ahead to exclude image data URLs.
#   5. .*            – any remaining characters.
#
# The regex is case‑insensitive and anchored to the start of the string,
# so it only flags URLs that begin with a risky scheme.
DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*[^:]+:(?!\s*data:image)',
    re.IGNORECASE
)

def has_script_scheme(url: str) -> bool:
    """
    Return True if the supplied URL string starts with a dangerous
    scheme (e.g., javascript:, vbscript:) and is not an image data URL.
    """
    if not isinstance(url, str):
        return False
    return bool(DANGEROUS_SCHEME_RE.match(url))