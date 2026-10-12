import re

# List of known dangerous URL schemes that should trigger a warning.
_DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'data',          # handled specially below
    'file',
    'ftp',
    'mailto',
    'ms-help',
    'ms-word',
    # add more schemes as needed
}

# Regular expression to extract the scheme from a URL.
# It allows optional leading whitespace and optional surrounding quotes or
# angle brackets that might be present in HTML attributes.
_SCHEME_RE = re.compile(r"""
    ^\s*                     # Optional leading whitespace
    (?:[\"\'<])?             # Optional opening quote or angle bracket
    (?P<scheme>[a-zA-Z][\w+.-]*):   # Scheme (letters, digits, _, +, ., -)
    """, re.VERBOSE | re.IGNORECASE)


def has_script_scheme(url: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme.

    The function checks the beginning of the input for a URL scheme and
    returns True if that scheme is considered risky.  Image data URLs (e.g.
    ``data:image/png;base64,...``) are excluded from the warning.

    Parameters
    ----------
    url : str
        The string to inspect.  It may contain whitespace, quotes, or angle
        brackets as commonly seen in HTML attributes.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected, otherwise ``False``.

    Notes
    -----
    * The check is case‑insensitive.
    * Only the scheme at the start of the string is considered; trailing
      content (e.g., parameters) does not affect the result.
    * The function intentionally ignores data URLs that start with
      ``data:image/`` because those are safe image sources.
    """
    if not isinstance(url, str):
        # Defensive: non‑string input cannot contain a scheme.
        return False

    match = _SCHEME_RE.match(url)
    if not match:
        # No scheme found.
        return False

    scheme = match.group('scheme').lower()

    if scheme == 'data':
        # Allow only image data URLs.  Anything else is dangerous.
        # We perform a simple prefix check to avoid regex overhead.
        data_prefix = url.lower().lstrip()
        return not data_prefix.startswith('data:image/')
    return scheme in _DANGEROUS_SCHEMES