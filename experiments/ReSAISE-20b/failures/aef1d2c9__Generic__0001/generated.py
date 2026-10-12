import re

# Regular expression to match dangerous URL schemes.
# We use a case‑insensitive pattern and allow optional whitespace before the scheme.
# The pattern captures the scheme name so we can handle `data:` specially.
_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(?P<scheme>javascript|vbscript|data)\b[^;]*:',
    re.IGNORECASE
)

def has_script_scheme(url: str) -> bool:
    """
    Determine whether *url* contains a risky URL scheme.

    Parameters
    ----------
    url : str
        The string to inspect. It may contain leading/trailing whitespace.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is found, otherwise ``False``.

    Notes
    -----
    * The function ignores a `data:` scheme that is an image data URI,
      e.g. ``data:image/png;base64,...``.
    * Only the schemes listed in :data:`_DANGEROUS_SCHEME_RE` are considered
      dangerous.  The list can be extended if needed.
    """
    match = _DANGEROUS_SCHEME_RE.match(url)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # If the scheme is 'data', check whether it is an image data URI.
    if scheme == 'data':
        # Extract the MIME type part between "data:" and the first ';'
        mime_part = url[5:].split(';', 1)[0].lower()
        # Accept only image MIME types as safe.
        if mime_part.startswith('image/'):
            return False
    # For javascript or vbscript (or any other dangerous scheme), flag it.
    return True