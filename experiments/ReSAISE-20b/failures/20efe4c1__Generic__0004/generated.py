import re

# Pre‑compile regexes for performance and clarity.
_DANGEROUS_SCHEMES_RE = re.compile(
    r'^\s*(?P<scheme>javascript|vbscript|data):', re.IGNORECASE
)
# Regex to detect a data URL that starts with an image MIME type.
_DATA_IMAGE_RE = re.compile(
    r'^data\s*:\s*image\/[a-zA-Z0-9.+-]+', re.IGNORECASE
)

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether *url_input* contains a potentially harmful URL scheme
    (e.g. javascript:, vbscript:) while ignoring image data URLs.

    Parameters
    ----------
    url_input : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if a harmful scheme is detected, otherwise ``False``.

    Notes
    -----
    * The function treats strings that start with a data URL containing an
      image MIME type as safe.
    * Leading and trailing whitespace are ignored.
    """
    if not isinstance(url_input, str):
        # Non‑string inputs are considered unsafe by default.
        return True

    match = _DANGEROUS_SCHEMES_RE.match(url_input)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # If the scheme is 'data', ensure it is an image data URL.
    if scheme == 'data':
        return not _DATA_IMAGE_RE.match(url_input)

    # For javascript or vbscript (or any other dangerous scheme), return True.
    return True