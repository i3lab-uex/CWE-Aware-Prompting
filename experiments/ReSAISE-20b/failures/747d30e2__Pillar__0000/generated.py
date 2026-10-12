import re

# Regular expression to match potentially malicious URL schemes.
# It captures the scheme part (e.g., javascript, jscript, vbscript) and
# allows optional whitespace before the colon.
_MALICIOUS_SCHEMES_RE = re.compile(
    r"""
    ^\s*                         # Optional leading whitespace
    (?P<scheme>                   # Capture the scheme name
        javascript
      | jscript
      | vbscript
    )
    \s*:\s*                       # Colon surrounded by optional whitespace
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Regular expression to detect a data URL that starts with an image MIME type.
_DATA_IMAGE_RE = re.compile(
    r"""
    ^\s*data:                    # Optional leading whitespace, then 'data:'
    (?P<mime>image/[^;]*?)       # MIME type starting with 'image/'
    ;                            # End of MIME part
    """,
    re.IGNORECASE | re.VERBOSE,
)

def is_javascript_scheme(s: str) -> bool:
    """
    Return True if the string contains a potentially malicious URL scheme
    (javascript, jscript, vbscript) but NOT if it is an image data URL.
    
    Parameters
    ----------
    s : str
        The string to test.

    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    """
    if not isinstance(s, str):
        # If the input is not a string we cannot reliably test it.
        return False

    # First check for data:image/... URLs and exclude them.
    if _DATA_IMAGE_RE.match(s):
        return False

    # Now check for malicious schemes.
    return bool(_MALICIOUS_SCHEMES_RE.match(s))