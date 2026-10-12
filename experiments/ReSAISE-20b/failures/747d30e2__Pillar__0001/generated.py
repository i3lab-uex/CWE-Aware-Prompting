import re

# Regular expression to detect potentially malicious URL schemes.
# It matches strings that start with optional whitespace, followed by
# one of the disallowed schemes (javascript, vbscript, jscript) and a colon.
# The pattern is case‑insensitive to catch variants like "JavaScript:" or "JAVAscript:".
# We explicitly ignore data URLs that start with 'data:image/' to avoid
# false positives for image data URIs.
_JS_SCHEME_RE = re.compile(
    r'^\s*(?:javascript|vbscript|jscript)\s*:', re.IGNORECASE
)

# Regular expression to detect image data URLs.
_DATA_IMAGE_RE = re.compile(
    r'^data\s*:\s*image\/', re.IGNORECASE
)


def is_javascript_scheme(s: str) -> bool:
    """
    Determine whether the supplied string contains a possibly malicious
    URL scheme such as javascript:, vbscript: or jscript:.

    Image data URLs (e.g., 'data:image/png;base64,...') are excluded
    from being flagged as malicious.

    Parameters
    ----------
    s : str
        The string to test.

    Returns
    -------
    bool
        ``True`` if the string begins with a disallowed scheme (excluding
        image data URLs), otherwise ``False``.
    """
    if not isinstance(s, str):
        # Non‑string inputs are considered non‑malicious in this context.
        return False

    # Exclude image data URLs first.
    if _DATA_IMAGE_RE.match(s):
        return False

    # Check for malicious schemes.
    return bool(_JS_SCHEME_RE.match(s))