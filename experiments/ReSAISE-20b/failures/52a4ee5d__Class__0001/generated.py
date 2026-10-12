import re

# Regex to match dangerous URL schemes (javascript, vbscript, data, etc.)
# We consider a scheme valid if it is followed by ':' and not part of a
# data:image/... URL. We also allow optional whitespace before the colon.
_DANGEROUS_SCHEMES = re.compile(
    r"""
    ^\s*                                   # optional leading whitespace
    (?:                                     # start group of dangerous schemes
        javascript | vbscript |
        data:                                # allow data URLs but we will filter image types
    )
    \s*:\s*                                 # colon surrounded by optional whitespace
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regex to detect a valid image data URL (data:image/*;base64,...)
_VALID_IMAGE_DATA_URL = re.compile(
    r"""
    ^\s*                                   # optional leading whitespace
    data:                                  # start of data URL
    image\/                                # MIME type starts with image/
    [^;]+                                   # subtype until semicolon
    ;\s*base64\s*,                          # base64 indicator and comma
    """,
    re.IGNORECASE | re.VERBOSE,
)

def detect_js_scheme(url_string: str) -> bool:
    """
    Detects potentially harmful URL schemes in a string.

    Args:
        url_string: The input string to inspect.

    Returns:
        True if the string contains a dangerous scheme (e.g., javascript:, vbscript:)
        that is not an image data URL. False otherwise.
    """
    if not isinstance(url_string, str):
        return False

    # First check for a valid image data URL; if so, it is safe.
    if _VALID_IMAGE_DATA_URL.match(url_string):
        return False

    # If it matches a dangerous scheme, flag as True.
    if _DANGEROUS_SCHEMES.match(url_string):
        return True

    # No dangerous scheme detected.
    return False