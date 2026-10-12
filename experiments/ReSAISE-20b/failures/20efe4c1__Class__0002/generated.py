import re

# Regular expression to detect dangerous URL schemes.
# It matches strings that start with a scheme like
#   javascript:, vbscript:, data: (excluding image/*),
# or any other scheme that is not a standard safe scheme.
# The regex ignores leading whitespace and allows optional
# surrounding quotes or brackets commonly used in HTML attributes.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                          # Optional leading whitespace
    (?:['"\(\[]?)                 # Optional opening quote or bracket
    (?P<scheme>                    # Capture the scheme part
        (?:[a-z][a-z0-9+\-.]*:)    # General scheme pattern
        |
        data:                      # Explicit data: scheme
    )
    (?P<url>[^'"\)\]\s]*)          # Rest of the URL (no whitespace or closing chars)
    """,
    re.IGNORECASE | re.VERBOSE
)

# Safe schemes that are generally acceptable.
_SAFE_SCHEMES = {
    'http:', 'https:', 'ftp:', 'ftps:',
    'mailto:', 'tel:', 'data:image/',  # allow only image data URLs
}

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Determine whether a string contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while ignoring safe image data URLs.

    Args:
        url_input (str): The string to examine for dangerous URL schemes.

    Returns:
        bool: True if a dangerous scheme is found, False otherwise.
    """
    if not isinstance(url_input, str):
        return False  # Non-string inputs are considered safe

    match = _DANGEROUS_SCHEME_RE.match(url_input)
    if not match:
        return False

    scheme = match.group('scheme').lower()
    url_part = match.group('url')

    # Check for allowed image data URLs
    if scheme == 'data:' and url_part.lower().startswith('image/'):
        return False

    # If scheme is in the safe list, it's fine
    if scheme in _SAFE_SCHEMES:
        return False

    # Anything else is considered dangerous
    return True