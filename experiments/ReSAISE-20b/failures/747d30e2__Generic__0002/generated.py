import re

def is_javascript_scheme(s: str) -> bool:
    """
    Detects potentially malicious URL schemes in a string, excluding image data URLs.

    Parameters
    ----------
    s : str
        The input string to check for malicious URL schemes.

    Returns
    -------
    bool
        True if the string contains a suspicious scheme such as javascript,
        jscript, vbscript, etc., and does not contain an image data URL.
        False otherwise.

    Notes
    -----
    * The function is intentionally conservative: it only flags strings that
      start with one of the known malicious schemes after optional whitespace.
    * Image data URLs (e.g., "data:image/png;base64,...") are explicitly ignored.
    * The check is case‑insensitive and tolerant of whitespace between the
      scheme delimiter and the colon.
    """
    if not isinstance(s, str):
        # Non‑string input is considered safe
        return False

    # Skip any string that contains an image data URL.
    if re.search(r'data\s*:\s*image', s, flags=re.IGNORECASE):
        return False

    # Regex to match suspicious schemes at the start of the string.
    # Allows optional whitespace before the scheme and optional
    # whitespace between the scheme name and the colon.
    suspicious_pattern = re.compile(
        r'^[\s]*'
        r'(?:javascript|jscript|vbscript)'
        r'\s*:',
        flags=re.IGNORECASE
    )

    return bool(suspicious_pattern.search(s))