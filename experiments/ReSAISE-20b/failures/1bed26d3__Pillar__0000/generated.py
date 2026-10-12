import re

# Regular expression to detect potentially dangerous URL schemes.
# It matches strings that start with a scheme followed by ':'
# (allowing optional whitespace before the scheme).
_DANGEROUS_SCHEME_RE = re.compile(r'^\s*(javascript|vbscript)\s*:', re.IGNORECASE)

# Regular expression to detect data URLs that reference images.
_DATA_IMAGE_RE = re.compile(r'^data\s*:\s*image\b', re.IGNORECASE)


def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether a given string contains a potentially harmful URL scheme
    (e.g., JavaScript, vbscript), while excluding image-based data URLs.

    Parameters
    ----------
    url_str : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if the string contains a dangerous scheme (except safe image data URLs),
        False otherwise.

    Notes
    -----
    - The function performs a simple, case‑insensitive check for the presence of
      "javascript:" or "vbscript:" at the beginning of the string (ignoring leading
      whitespace).  It does not attempt to parse or validate the rest of the URL.
    - Image-based data URLs (e.g., "data:image/png;base64,...") are explicitly
      excluded from being flagged as dangerous.
    - This implementation is intentionally conservative to avoid false positives,
      but it may miss more complex or obfuscated attacks.  For production use,
      consider a dedicated URL sanitisation library.
    """
    if not isinstance(url_str, str):
        # If the input is not a string we cannot safely analyse it.
        return False

    # Normalise whitespace and case for matching
    stripped = url_str.lstrip()

    # Exclude image data URLs first.
    if _DATA_IMAGE_RE.match(stripped):
        return False

    # Check for dangerous schemes.
    if _DANGEROUS_SCHEME_RE.match(stripped):
        return True

    return False