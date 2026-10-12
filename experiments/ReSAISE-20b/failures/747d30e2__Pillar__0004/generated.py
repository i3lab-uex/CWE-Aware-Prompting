import re

# Regular expression to detect potentially malicious URL schemes.
# It matches strings that start (after optional whitespace) with
# 'javascript', 'jscript' or 'vbscript', followed by a colon.
_JS_URL_SCHEME_RE = re.compile(r'^\s*(?:javascript|jscript|vbscript)\b', flags=re.I)

def is_javascript_scheme(s: str) -> bool:
    """
    Detect if the supplied string contains a potentially malicious URL scheme
    such as javascript:, jscript: or vbscript:.  Image data URLs (e.g.
    data:image/...) are explicitly excluded.

    Parameters
    ----------
    s : str
        The string to test for malicious URL schemes.

    Returns
    -------
    bool
        True if a potentially dangerous scheme is present; False otherwise.
    """
    if not isinstance(s, str):
        # Non‑string inputs are considered safe (no scheme to check).
        return False

    # Exclude image data URLs which are legitimate use cases.
    if s.lower().startswith('data:image/'):
        return False

    # Use the compiled regex to test for a malicious scheme at the start.
    return bool(_JS_URL_SCHEME_RE.match(s))