import re

# Regular expression that matches a dangerous scheme at the start of a string.
# It is case‑insensitive and ignores leading whitespace.  The pattern
# captures the scheme part (e.g., "javascript" or "vbscript") followed by a colon.
DANGEROUS_SCHEME_RE = re.compile(r'^\s*(javascript|vbscript)\s*:', re.IGNORECASE)

# Regular expression that matches an image data URL (which is considered safe).
# The pattern allows any "data:image/..." scheme and ignores leading whitespace.
SAFE_IMAGE_DATA_URL_RE = re.compile(r'^\s*data:image\/', re.IGNORECASE)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Determine whether *uri_str* contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Parameters
    ----------
    uri_str : str
        The string to examine.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is present; otherwise ``False``.

    Notes
    -----
    The function performs only a simple, well‑formedness‑agnostic check.
    It does not attempt to fully parse the URI; therefore it is resilient
    against malformed inputs but may still flag URLs that contain a
    dangerous scheme as part of a longer, more complex URI.
    """
    # If the string is a safe image data URL, immediately return False.
    if SAFE_IMAGE_DATA_URL_RE.match(uri_str):
        return False

    # If the string starts with a dangerous scheme, flag it.
    if DANGEROUS_SCHEME_RE.match(uri_str):
        return True

    # No dangerous scheme detected.
    return False