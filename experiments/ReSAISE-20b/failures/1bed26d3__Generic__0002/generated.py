import re

# Regular expression that matches dangerous URL schemes.
# It captures common script based schemes and any data: URI that is not an image.
_DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                   # Optional leading whitespace
    (?:
        (?:javascript|vbscript)            # Classic script schemes
      | data:                             # Data URIs that are not images
          (?!image/)                      # Negative look‑ahead: reject image/
    )
    \s*:
    """,
    re.IGNORECASE | re.VERBOSE
)

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine if a string contains a potentially dangerous URL scheme
    (e.g., javascript:, vbscript:) while excluding safe image data URLs.

    Parameters:
        url_str (str): The string to inspect.

    Returns:
        bool: True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(url_str, str):
        return False  # Non‑string inputs are considered safe

    # Search for the dangerous pattern
    return bool(_DANGEROUS_SCHEME_RE.match(url_str))