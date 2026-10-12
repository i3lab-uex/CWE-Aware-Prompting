import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects potentially malicious URL schemes in a string, excluding valid image data URLs.

    Parameters
    ----------
    url_string : str
        The input string to inspect.

    Returns
    -------
    bool
        True if a dangerous URL scheme is found; False otherwise.

    Notes
    -----
    The function looks for the following patterns (case‑insensitive):

        * javascript:      optionally preceded by whitespace
        * vbscript:        optionally preceded by whitespace
        * data:            but NOT followed by 'image/'

    It does not raise exceptions for normal input; any regex errors will propagate
    as re.error.
    """
    if not isinstance(url_string, str):
        return False

    # Patterns for dangerous schemes
    js_vb_pattern = re.compile(r'(?i)\b(?:javascript|vbscript)\s*:', re.IGNORECASE)
    # data: scheme that is NOT an image
    data_non_image_pattern = re.compile(r'(?i)data\s*:(?!image/)', re.IGNORECASE)

    # Search for any dangerous scheme
    if js_vb_pattern.search(url_string):
        return True

    # Search for non‑image data URLs
    if data_non_image_pattern.search(url_string):
        return True

    return False