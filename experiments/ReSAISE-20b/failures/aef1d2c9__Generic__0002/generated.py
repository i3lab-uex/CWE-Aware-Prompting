import re

def has_script_scheme(url: str) -> bool:
    """
    Detects if a string contains a dangerous URL scheme (e.g. javascript:, vbscript:)
    while ignoring safe data URLs for images.

    Parameters
    ----------
    url : str
        The URL string to inspect.

    Returns
    -------
    bool
        True if a dangerous scheme is present, False otherwise.
    """
    # Quick normalisation
    if not isinstance(url, str):
        return False

    url_stripped = url.strip().lower()

    # Detect explicit javascript: or vbscript: schemes (case‑insensitive)
    if re.match(r'^(javascript|vbscript)\b', url_stripped, flags=re.IGNORECASE):
        return True

    # Detect data: URLs that are not image/* (e.g. data:text/html,...)
    if url_stripped.startswith('data:'):
        # If it is an image data URL, we consider it safe
        if re.match(r'^data:image/', url_stripped, flags=re.IGNORECASE):
            return False
        # Any other data: scheme is considered risky
        return True

    return False