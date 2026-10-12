import re

# Regular expression that matches potentially dangerous URL schemes.
# It is case‑insensitive and allows optional whitespace before the colon.
# We explicitly exclude data URLs that start with "data:image".
_DANGEROUS_SCHEMES_RE = re.compile(
    r'''
    ^\s*                                   # optional leading whitespace
    (?:                                     # non‑capturing group for schemes
        javascript: |
        vbscript: |
        lscript: |
        mailto:   # often abused, but still potentially dangerous
    )
    ''',
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression that matches a valid image data URL.
_DATA_IMAGE_URL_RE = re.compile(
    r'''
    ^\s*                                   # optional leading whitespace
    data:image/                             # image MIME type prefix
    [\w+\-\.]+                              # image subtype (e.g., png, jpeg)
    ;base64\s*                              
    ''',
    re.IGNORECASE | re.VERBOSE,
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect whether a string contains a potentially dangerous URL scheme
    (javascript:, vbscript:, etc.) while ignoring valid image data URLs.

    Parameters:
        url_string (str): The string to examine.

    Returns:
        bool: True if a dangerous scheme is detected; False otherwise.
    """
    # Quick reject if the string is not a string type
    if not isinstance(url_string, str):
        return False

    # Ignore valid image data URLs
    if _DATA_IMAGE_URL_RE.match(url_string):
        return False

    # Check for dangerous schemes
    return bool(_DANGEROUS_SCHEMES_RE.match(url_string))