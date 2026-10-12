import re

# Regular expression to detect potentially dangerous URL schemes.
# It matches any string that starts with a scheme followed by a colon,
# where the scheme is not 'data:image' (case‑insensitive).
# Common dangerous schemes include javascript, vbscript, data, and others.
_DANGEROUS_SCHEME_RE = re.compile(
    r'^\s*(?:(?!data:image\b)[a-z][a-z0-9+.-]*):',
    re.IGNORECASE
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect if a string contains a potentially harmful URL scheme.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string involves a potentially harmful URL scheme,
        except for valid image data URLs; False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading/trailing whitespace before matching.
    stripped = url_string.strip()

    # If the string starts with a dangerous scheme (excluding data:image),
    # return True.
    if _DANGEROUS_SCHEME_RE.match(stripped):
        return True

    return False