import re

# Regular expression that matches dangerous URL schemes.
# It looks for a scheme at the beginning of the string, followed by ':',
# and ignores valid image data URLs (data:image/...).
_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(?P<scheme>[a-z][a-z0-9+\-.]*):',
    re.IGNORECASE
)

# Set of schemes that are considered safe or explicitly allowed.
_SAFE_SCHEMES = {
    'http',
    'https',
    'ftp',
    'ftps',
    'mailto',
    'tel',
    # data URLs are handled separately; see below
}

def has_script_scheme(url: str) -> bool:
    """
    Determine whether *url* contains a risky scheme such as javascript:, vbscript:, or
    other potentially malicious schemes. Valid image data URLs (data:image/...) are
    excluded from the check.

    Parameters
    ----------
    url : str
        The input string to be inspected for potentially malicious URL schemes.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected; otherwise ``False``.

    Notes
    -----
    - The function uses a case‑insensitive regular expression to capture the scheme.
    - A data URL that starts with ``data:image/`` is considered safe and does not
      trigger a True result.
    - The function does **not** raise exceptions for normal usage; any regex
      compilation errors would be raised during module import time.
    """
    if not isinstance(url, str):
        # Non‑string input cannot contain a URL scheme.
        return False

    match = _DANGEROUS_SCHEME_RE.match(url)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # Exclude safe schemes.
    if scheme in _SAFE_SCHEMES:
        return False

    # Exclude valid image data URLs.
    if scheme == 'data':
        # Check for the specific pattern: data:image/<type>;base64,...
        if re.match(r'^\s*data:image/\w+', url, re.IGNORECASE):
            return False

    # Anything else is considered dangerous.
    return True