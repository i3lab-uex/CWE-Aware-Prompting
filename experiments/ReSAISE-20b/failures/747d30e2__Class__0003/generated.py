import re

# Regular expression that matches a URL scheme beginning with one of the
# potentially malicious schemes. The pattern intentionally ignores data URLs
# that start with "data:image/".
#
#   ^\s*                     # Optional leading whitespace
#   (javascript|jscript|vbscript)  # Malicious scheme names
#   \s*:\s*                  # Optional whitespace around the colon separator
#
# This regex is deliberately simple to avoid over‑matching and to remain
# efficient. It is case‑insensitive.
MALICIOUS_SCHEME_RE = re.compile(r'^\s*(javascript|jscript|vbscript)\s*:', re.IGNORECASE)


def is_javascript_scheme(s: str) -> bool:
    """
    Detect whether a string contains a possibly malicious URL scheme
    (javascript, jscript, vbscript) while excluding image data URLs.

    Parameters:
        s: The string to inspect.

    Returns:
        True if the string starts with a malicious scheme, False otherwise.
    """
    # Reject data:image URLs explicitly – they are allowed and safe for images
    if s.lower().startswith('data:image/'):
        return False

    # Check for malicious schemes at the beginning of the string
    return bool(MALICIOUS_SCHEME_RE.match(s))