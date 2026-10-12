import re

# Regular expression that matches common dangerous URL schemes.
# It looks for a scheme at the start of the string, followed by ':'.
# The `^` anchors the match to the beginning; optional whitespace is ignored.
DANGEROUS_SCHEME_RE = re.compile(r'^\s*(javascript|vbscript|data)\b', re.IGNORECASE)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect if a string contains a potentially dangerous URL scheme.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        aside from valid image data URLs; False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace for accurate matching.
    stripped = url_string.strip()

    match = DANGEROUS_SCHEME_RE.match(stripped)
    if not match:
        return False

    scheme = match.group(1).lower()

    # `data:` URLs are only dangerous if they are not image data.
    if scheme == 'data':
        # A safe image data URL looks like: data:image/png;base64,...
        # Anything else is considered potentially dangerous.
        if stripped.lower().startswith('data:image'):
            return False
        else:
            return True

    # Any other matched scheme is considered dangerous.
    return True