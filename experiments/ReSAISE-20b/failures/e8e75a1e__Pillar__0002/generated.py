import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects potentially malicious URL schemes in a string.

    Parameters
    ----------
    url_string : str
        The input string to inspect for dangerous URL schemes.

    Returns
    -------
    bool
        True if a risky scheme (e.g., javascript:, vbscript:) is found; otherwise False.

    Notes
    -----
    - Valid image data URLs (e.g., "data:image/png;base64,...") are ignored because
      they start with the scheme 'data:' which is explicitly excluded from the
      dangerous list.
    - The function uses a case‑insensitive search and matches only whole words
      followed by a colon to avoid false positives in the middle of words.
    """
    # List of known dangerous schemes
    DANGEROUS_SCHEMES = (r"javascript", r"vbscript")

    # Compile a regex that matches any of the dangerous schemes followed by a colon.
    pattern = re.compile(r"\b(" + r"|".join(DANGEROUS_SCHEMES) + r"):", re.IGNORECASE)

    try:
        return bool(pattern.search(url_string))
    except re.error:
        # In the unlikely event that the regex fails, assume no malicious scheme.
        return False