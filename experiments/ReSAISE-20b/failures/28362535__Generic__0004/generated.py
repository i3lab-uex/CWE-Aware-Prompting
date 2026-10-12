import re

# Regular expression patterns for dangerous schemes.
# The pattern is case‑insensitive and allows optional leading whitespace.
DANGEROUS_SCHEMES = re.compile(r'^\s*(javascript|vbscript):', re.IGNORECASE)

# Pattern to detect image data URLs (e.g., data:image/png;base64,...)
IMAGE_DATA_URL = re.compile(r'^data\s*:\s*image\/[a-zA-Z0-9+\.\-_]+', re.IGNORECASE)


def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether ``input_url`` contains a potentially harmful URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    input_url : str
        The string to examine for dangerous URL schemes.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected (excluding safe image data URLs),
        otherwise ``False``.

    Notes
    -----
    * The function treats the following schemes as dangerous:
      ``javascript:`` and ``vbscript:``, case‑insensitively.
    * Any URL starting with ``data:`` that is **not** an image data URI
      (e.g., ``data:text/html,``) is considered dangerous.
    * Leading whitespace before the scheme is ignored.
    """
    # Normalize leading whitespace for easier matching
    stripped = input_url.lstrip()

    # Check for data: URLs first because they have special handling
    if stripped.lower().startswith('data:'):
        # If it is an image data URL, consider it safe
        if IMAGE_DATA_URL.match(stripped):
            return False
        # Any other data: URL is considered malicious
        return True

    # Check for dangerous schemes like javascript: or vbscript:
    if DANGEROUS_SCHEMES.match(stripped):
        return True

    # No dangerous scheme detected
    return False