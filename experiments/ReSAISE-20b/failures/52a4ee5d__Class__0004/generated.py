import re

# Regular expression that matches a URI scheme followed by a colon.
_SCHEME_RE = re.compile(r'^\s*([a-z][a-z0-9+\-.]*):', re.IGNORECASE)

# Set of schemes considered dangerous for typical web contexts.
_DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'data',          # handled separately below
    'file',
    'ftp',
    'gopher',
    'mailto',        # not usually dangerous, but can be abused
}

# Set of allowed data URL sub‑schemes (e.g., image/*).
_ALLOWED_DATA_SUBSCHEMES = {'image'}

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect if *url_string* contains a potentially harmful URL scheme.

    The function returns ``True`` when the string starts with a known
    dangerous scheme (e.g. javascript, vbscript) and is **not** an image
    data URL such as ``data:image/png;base64,...``.  It is case‑insensitive
    and ignores leading whitespace.

    Parameters
    ----------
    url_string : str
        The URL string to examine.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is present; otherwise ``False``.

    Notes
    -----
    - The check is intentionally conservative: any scheme not in the
      ``_DANGEROUS_SCHEMES`` set is considered safe.
    - Image data URLs are allowed because they are widely used for
      inline images and do not execute code.
    """
    if not isinstance(url_string, str):
        return False

    match = _SCHEME_RE.match(url_string)
    if not match:
        # No scheme present.
        return False

    scheme = match.group(1).lower()

    if scheme not in _DANGEROUS_SCHEMES:
        return False

    # Special handling for data URLs: only allow image/* sub‑types.
    if scheme == 'data':
        # Grab the MIME type part (before any ';' or ',').
        mime_type = url_string.split(':', 1)[1].split(';', 1)[0]
        if mime_type.lower().startswith('image/'):
            return False
        # Any other data: sub‑type is considered dangerous.
        return True

    # For all other schemes in the dangerous set, flag as unsafe.
    return True