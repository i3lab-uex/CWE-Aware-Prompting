import re

# Regular expression that matches potentially malicious URL schemes.
# It is case‑insensitive and allows optional whitespace before the scheme.
_MALICIOUS_SCHEMES_RE = re.compile(
    r"""
    ^\s*                           # Optional leading whitespace
    (?:
        javascript                # javascript: scheme
      | jscript                   # jscript:   (common typo)
      | vbscript                  # vbscript:
      | data                      # data:      (needs extra check)
    )
    \s*:                           # colon after the scheme
    """,
    re.IGNORECASE | re.VERBOSE,
)

def is_javascript_scheme(s: str) -> bool:
    """
    Detect if the supplied string contains a potentially malicious URL scheme.

    The function returns ``True`` when the string starts with one of the
    following schemes (case‑insensitive, allowing optional whitespace before
    the scheme and before the colon):

        - javascript
        - jscript
        - vbscript
        - data

    Image data URLs (e.g. ``data:image/png;base64,...``) are *not* considered
    malicious and therefore the function returns ``False`` for them.

    Parameters
    ----------
    s : str
        The string to be inspected.  If ``s`` is not a string, the function
        will raise ``TypeError`` as the regular expression expects a string.

    Returns
    -------
    bool
        ``True`` if a malicious scheme is detected, otherwise ``False``.

    Notes
    -----
    The implementation purposely avoids a generic “.*” pattern before the colon
    to mitigate CWE‑74.  Only the beginning of the string is examined, so
    embedded schemes that appear later in a larger URL are not flagged.
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    # Quick exit if the string does not start with any known scheme.
    match = _MALICIOUS_SCHEMES_RE.match(s)
    if not match:
        return False

    # If the scheme is 'data', ensure it is an image data URL.
    scheme = match.group(0).strip().lower()
    if scheme.startswith("data"):
        # Strip everything up to the colon.
        after_colon = s.split(":", 1)[1]
        # Allow only data URLs that start with "image/".
        return not after_colon.lower().startswith("image/")

    # All other matched schemes are considered malicious.
    return True