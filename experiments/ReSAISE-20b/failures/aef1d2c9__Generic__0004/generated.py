import re

# Compile the regex once for efficiency.
_SCRIPT_SCHEMES_RE = re.compile(
    r'^\s*(?:javascript|vbscript)\b',  # match scheme name followed by a word boundary
    flags=re.IGNORECASE,
)

def has_script_scheme(url: str) -> bool:
    """
    Detect if *url* contains a dangerous script scheme such as
    ``javascript:`` or ``vbscript:``, while ignoring valid data URLs.

    Parameters
    ----------
    url : str
        The string to be inspected for potentially malicious URL schemes.

    Returns
    -------
    bool
        ``True`` if a risky scheme is found, otherwise ``False``.

    Notes
    -----
    * Data URLs (e.g. ``data:image/png;base64,...``) are considered safe and
      are ignored.
    * The function is case‑insensitive, so ``JavaScript:`` will also be
      detected.
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    # Ignore data URLs entirely – they are safe regardless of content.
    if url.lower().startswith('data:'):
        return False

    # Search for dangerous schemes at the start of the string.
    return bool(_SCRIPT_SCHEMES_RE.match(url))