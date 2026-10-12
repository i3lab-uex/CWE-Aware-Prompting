import re

def analyze_scheme(url: str) -> bool:
    """
    Detect potentially dangerous URL schemes (e.g., javascript:, vbscript:)
    while ignoring valid image data URLs.

    Parameters
    ----------
    url : str
        The URL string to examine.

    Returns
    -------
    bool
        True if the URL contains a dangerous scheme, False otherwise.
    """
    # Return False for empty or non-string inputs
    if not isinstance(url, str) or not url:
        return False

    # Strip leading/trailing whitespace
    url = url.strip()

    # Regular expression to match dangerous schemes:
    #   - starts with a word followed by colon
    #   - excludes 'data:image' URLs
    dangerous_pattern = re.compile(
        r"""(?xi)              # case-insensitive, verbose
            ^\s*                # optional leading whitespace
            (?!data:image)      # negative lookahead for image data URLs
            (\w+):              # scheme (letters, digits, underscore) followed by colon
        """,
        re.UNICODE
    )

    match = dangerous_pattern.match(url)
    if not match:
        return False

    scheme = match.group(1).lower()
    # List of known potentially dangerous schemes
    dangerous_schemes = {
        'javascript',
        'vbscript',
        'data',          # generic data: scheme is risky unless image
        'file',
        'mailto',        # could be abused in certain contexts
    }

    return scheme in dangerous_schemes