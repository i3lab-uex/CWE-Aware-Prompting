import re

# Regular expressions for dangerous schemes.
_DANGEROUS_SCHEMES = [
    re.compile(r'^\s*javascript\s*:', re.IGNORECASE),
    re.compile(r'^\s*vbscript\s*:', re.IGNORECASE),
]

# Regular expression for data URLs that are safe (image/*).
_SAFE_DATA_URL = re.compile(
    r'^\s*data\s*:image\/[a-z0-9.+-]+',
    re.IGNORECASE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether the supplied string contains a potentially malicious
    URL scheme (e.g., javascript:, vbscript:) while excluding safe image
    data URLs.

    Parameters
    ----------
    input_url : str
        The string to be examined for potentially dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected; False otherwise.
    """
    if not isinstance(input_url, str):
        # Non-string inputs are considered unsafe to avoid subtle bugs.
        return True

    url = input_url.strip()

    # 1. Check for explicitly dangerous schemes.
    for pattern in _DANGEROUS_SCHEMES:
        if pattern.match(url):
            return True

    # 2. Handle data URLs: only safe if image/*.
    if url.lower().startswith('data:'):
        # If the data URL starts with image/*, treat it as safe.
        if _SAFE_DATA_URL.match(url):
            return False
        # Any other data URL is considered dangerous.
        return True

    return False