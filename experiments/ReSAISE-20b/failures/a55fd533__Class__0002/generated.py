import re

# Regular expression to detect dangerous URL schemes.
#
# The pattern matches strings that contain a scheme part followed by a colon,
# where the scheme is one of:
#   - javascript
#   - vbscript
#   - data (but only when not followed by 'image/')
#
# The pattern is case‑insensitive and allows optional whitespace around the
# colon, as attackers often use variations such as "javascript : void(0)".
#
# Examples that should return True:
#   "javascript:alert('XSS')"
#   "vbscript:MsgBox(\"Hello\")"
#   "data:text/html;base64,..." (non‑image data URLs)
#
# Examples that should return False:
#   "data:image/png;base64,iVBORw0KGgo..."
#   "http://example.com"
#   "https://example.org/path"

_DANGEROUS_SCHEME_RE = re.compile(
    r'''
    (?i)                    # case‑insensitive
    \b                      # word boundary to avoid matching substrings
    (?:javascript|vbscript)  # explicit dangerous schemes
    \s*:\s*                 # optional whitespace around the colon
    |                       # OR
    data\s*:                # data: scheme (case‑insensitive)
    (?!image/)\s*           # negative lookahead to exclude image data URLs
    ''',
    re.VERBOSE,
)

def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Determine whether the supplied string contains a risky URL scheme.

    Parameters
    ----------
    user_input : str
        The input string to be inspected for potentially malicious URL schemes.

    Returns
    -------
    bool
        True if the string contains any dangerous URL schemes (e.g. javascript,
        vbscript, or non‑image data URLs). False otherwise.

    Notes
    -----
    The function is intentionally tolerant of whitespace variations to catch
    common obfuscation techniques.  It specifically ignores data URLs that
    reference images (``data:image/...``) because these are typically safe in
    HTML contexts such as <img src="">.
    """
    if not isinstance(user_input, str):
        # Defensive programming: non‑string inputs are considered safe.
        return False

    # Use search to detect any occurrence of a dangerous scheme in the string.
    return bool(_DANGEROUS_SCHEME_RE.search(user_input))