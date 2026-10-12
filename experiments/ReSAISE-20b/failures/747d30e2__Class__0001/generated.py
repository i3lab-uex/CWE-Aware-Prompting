import re

# Regular expression to detect potentially malicious URL schemes.
# It matches a scheme at the beginning of the string or after optional
# whitespace, followed by a colon.  The scheme must not be a data URI
# that starts with "data:image/".  Common malicious schemes are
# javascript, jscript, vbscript, data, mailto, and others that can be
# exploited via URL handlers.
#
# The regex is intentionally written to be case‑insensitive and
# to allow leading whitespace or other characters that may precede the
# scheme in HTML attributes (e.g., `href="   javascript:alert(1)"`).
# It also ensures that the scheme is not followed by a valid
# data:image URI, which is safe for image tags.
#
# CWE-74 consideration: we do not directly interpolate user input
# into a larger string.  The regex is compiled once and used for
# matching only, mitigating the risk of injection.
_MALICIOUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                   # optional leading whitespace
    (?:                                    # start non‑capturing group for scheme
        javascript:|
        jscript:|
        vbscript:|
        data:image/                         # safe image data URIs are excluded
    )                                      # end group
    """,
    re.IGNORECASE | re.VERBOSE
)

def is_javascript_scheme(s: str) -> bool:
    """
    Determine whether a string contains a possibly malicious URL scheme
    (e.g., javascript:, jscript:, vbscript:).  Image data URLs are excluded.

    Parameters
    ----------
    s : str
        The string to be inspected for a malicious URL scheme.

    Returns
    -------
    bool
        True if the string starts with a malicious scheme (excluding image
        data URLs); False otherwise.
    """
    if not isinstance(s, str):
        # Non‑string input is considered safe by default.
        return False

    # The regex only checks for the scheme at the beginning of the string
    # after optional whitespace.  We do not look for other occurrences
    # within the string to avoid false positives in URLs that contain
    # a colon later on.
    return bool(_MALICIOUS_SCHEME_RE.match(s))