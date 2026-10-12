import re

# Regular expression to detect dangerous URL schemes.
# It matches the start of a string (ignoring leading whitespace) followed by
# either 'javascript:' or 'vbscript:'.  The pattern is case‑insensitive.
_DANGEROUS_SCHEME_RE = re.compile(r'^\s*(?:javascript:|vbscript:)', re.IGNORECASE)

def analyze_scheme(url: str) -> bool:
    """
    Determine whether a string contains a potentially harmful URL scheme,
    excluding valid image data URLs.

    Parameters
    ----------
    url : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if the string involves a potentially harmful URL scheme
        (e.g., 'javascript:' or 'vbscript:'); ``False`` otherwise.
    """
    if not isinstance(url, str):
        # Non‑string inputs are considered safe by default.
        return False

    # Strip leading/trailing whitespace for a cleaner match
    trimmed = url.strip()

    # If the string starts with a dangerous scheme, return True.
    if _DANGEROUS_SCHEME_RE.match(trimmed):
        return True

    # All other cases are considered safe.
    return False