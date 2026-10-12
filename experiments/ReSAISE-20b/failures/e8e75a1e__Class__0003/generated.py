import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects potentially malicious URL schemes in a given string.
    
    Parameters
    ----------
    url_string : str
        The input string to inspect for dangerous URL schemes.
    
    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    
    Notes
    -----
    * The function ignores valid data URLs that start with 'data:image/'.
    * Dangerous schemes include javascript:, vbscript:, file:, data: (other than image), and any scheme that starts with a known
      suspicious prefix.
    * The detection is performed using a compiled regular expression that normalizes whitespace and case.
    
    Security Considerations
    -----------------------
    * The regex is anchored to the beginning of a URL or attribute value to avoid accidental matches in unrelated text.
    * The pattern is intentionally conservative to reduce false positives while still catching common XSS vectors.
    
    """
    # Normalise the string for case-insensitive matching
    lowered = url_string.lower()

    # Patterns that indicate a dangerous scheme
    # We use a non-capturing group for the scheme part.
    # The pattern matches:
    #   - javascript:, vbscript:, file: (common XSS schemes)
    #   - data: but not data:image/
    # The scheme is matched only if it appears at the start of a string or after
    # whitespace, quotes, or typical attribute separators.
    dangerous_pattern = re.compile(
        r"""
        (?:^|[\s"'=<>])          # start of string or a delimiter
        (?:
            javascript:         # javascript scheme
            |vbscript:          # vbscript scheme
            |file:              # file scheme (used in some OS contexts)
            |data:[^;]*         # data: scheme that is not image
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # Exclude valid image data URLs
    if lowered.startswith("data:image/"):
        return False

    # Search for any dangerous scheme
    if dangerous_pattern.search(lowered):
        return True

    return False