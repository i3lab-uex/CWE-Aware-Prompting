import re

# Regular expressions used to detect dangerous schemes.
_DANGEROUS_SCHEMES_RE = re.compile(r'^(javascript|vbscript):', re.IGNORECASE)
_DATA_SCHEME_RE = re.compile(r'^data:', re.IGNORECASE)
_SAFE_IMAGE_DATA_RE = re.compile(r'^data:image/', re.IGNORECASE)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the supplied URL contains a potentially harmful scheme
    (e.g., javascript:, vbscript:). Image-based data URLs are considered safe.

    Args:
        input_url (str): The URL string to inspect.

    Returns:
        bool: True if a dangerous scheme is detected (excluding safe image data URLs),
              False otherwise.
    """
    # Normalise whitespace and leading/trailing spaces
    url = input_url.strip()

    # Check for the most obvious dangerous schemes first.
    if _DANGEROUS_SCHEMES_RE.match(url):
        return True

    # Handle data URLs separately: only non‑image data schemes are considered malicious.
    if _DATA_SCHEME_RE.match(url):
        # Safe if the data URL is an image.
        return not _SAFE_IMAGE_DATA_RE.match(url)

    # No dangerous scheme found
    return False