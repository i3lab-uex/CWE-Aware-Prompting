import re

# Regular expressions for dangerous URL schemes.
_DANGEROUS_SCHEMES_RE = re.compile(
    r'^\s*(?:javascript|vbscript)\s*:',  # matches "javascript:" or "vbscript:" (case‑insensitive)
    re.IGNORECASE
)

# Regular expression for data URLs that reference images.
_IMAGE_DATA_URL_RE = re.compile(
    r'^\s*data\s*:\s*(?:image/(?:png|jpeg|gif|bmp|webp))\s*;',
    re.IGNORECASE
)

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Detects whether a string contains a potentially dangerous URL scheme.

    The function checks for `javascript:` or `vbscript:` schemes (case‑insensitive).
    It also considers data URLs that are not image-based as dangerous.
    Image data URLs (`data:image/*;...`) are explicitly ignored.

    Parameters
    ----------
    uri_str : str
        The URI string to examine.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme (excluding safe image data URLs),
        otherwise ``False``.

    Notes
    -----
    - The function is tolerant to leading whitespace and optional spaces before the colon.
    - It does not attempt to fully parse or validate URIs; it only looks for known dangerous patterns.
    - If the input is not a string, ``TypeError`` will be raised by the regex engine.
    """
    # Quick check for image data URLs; these are considered safe.
    if _IMAGE_DATA_URL_RE.match(uri_str):
        return False

    # Check for dangerous schemes.
    if _DANGEROUS_SCHEMES_RE.match(uri_str):
        return True

    # Also flag non‑image data URLs as dangerous (e.g., data:text/html;...).
    if re.match(r'^\s*data\s*:', uri_str, re.IGNORECASE):
        return True

    return False