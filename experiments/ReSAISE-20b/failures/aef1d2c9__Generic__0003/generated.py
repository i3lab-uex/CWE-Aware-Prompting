import re

def has_script_scheme(url: str) -> bool:
    """
    Detect if a URL string contains a dangerous scheme such as
    'javascript:' or 'vbscript:'.  Valid image data URLs (e.g.
    data:image/png;base64,...) are excluded from the check.

    Parameters
    ----------
    url : str
        The string to inspect for risky URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    """
    # Strip leading/trailing whitespace
    url = url.strip()

    # Pattern to capture the scheme part (everything before the first ':')
    scheme_pattern = re.compile(r'^(?P<scheme>[^:]+)', re.IGNORECASE)

    match = scheme_pattern.match(url)
    if not match:
        return False

    scheme = match.group('scheme').lower()

    # Allow 'data:' URLs only if they are image types
    if scheme == 'data':
        # Check for data:image/... format
        data_pattern = re.compile(r'^data\s*:\s*image\/', re.IGNORECASE)
        return not data_pattern.match(url)

    # Dangerous schemes list
    dangerous_schemes = {'javascript', 'vbscript'}

    return scheme in dangerous_schemes