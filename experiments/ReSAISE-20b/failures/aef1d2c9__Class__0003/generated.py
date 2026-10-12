import re

# Regular expression to extract the scheme from a URL.
# It captures any sequence of non‑colon, non‑slash characters at the beginning
# (optionally preceded by whitespace) as the scheme.
_SCHEME_RE = re.compile(r'^\s*([^:/?#]+)', re.IGNORECASE)

# Set of schemes that are considered dangerous.
_DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'data',        # handled specially below
    'file',
    'ftp',
    'mailto',
}

def has_script_scheme(url: str) -> bool:
    """
    Detect whether a URL contains a potentially dangerous scheme.

    Parameters
    ----------
    url : str
        The string to inspect for a malicious URL scheme.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme, otherwise ``False``.

    Notes
    -----
    * A data URI that starts with ``data:image/`` is considered safe and ignored.
    * The function performs a case‑insensitive check on the scheme part of the URL.
    """
    if not isinstance(url, str):
        # If the input is not a string we cannot parse it safely.
        return False

    match = _SCHEME_RE.match(url)
    if not match:
        # No scheme found (e.g., a relative path); nothing to flag.
        return False

    scheme = match.group(1).lower()

    # Exclude safe data URLs that contain an image.
    if scheme == 'data':
        # Check for a valid image data URL: data:image/<type>;base64,...
        # We consider any 'image/' substring after the initial 'data:' safe.
        if re.search(r'data\s*:\s*image\/', url, re.IGNORECASE):
            return False

    # If the scheme is in our list of dangerous schemes, flag it.
    if scheme in _DANGEROUS_SCHEMES:
        return True

    # All other schemes are considered safe for this check.
    return False