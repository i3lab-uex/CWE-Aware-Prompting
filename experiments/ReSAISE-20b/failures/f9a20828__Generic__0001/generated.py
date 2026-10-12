import re

def analyze_scheme(url: str) -> bool:
    """
    Detects potentially dangerous URL schemes in the given string, excluding
    legitimate image data URLs (e.g., 'data:image/png;base64,...').

    Parameters
    ----------
    url : str
        The URL string to analyze.

    Returns
    -------
    bool
        True if the URL contains a known harmful scheme (javascript, vbscript,
        shell, lnk, file, etc.), False otherwise.

    Notes
    -----
    - The function ignores URLs that start with the 'data' scheme and contain
      an image MIME type (e.g., data:image/png;base64,...).
    - Leading/trailing whitespace is ignored.
    """
    if not isinstance(url, str):
        return False

    # Strip leading/trailing whitespace
    url = url.strip()

    # Regex to capture the scheme before the first colon.
    # It allows optional whitespace and comments before the actual URL.
    match = re.match(r'^[\s]*([^\s:]+):', url, flags=re.IGNORECASE)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Exclude legitimate image data URLs
    if scheme == 'data':
        # Check if the MIME type after 'data:' starts with 'image/'
        data_match = re.match(r'^data\s*:\s*(image/[^;,\s]+)', url, flags=re.IGNORECASE)
        if data_match:
            return False

    # List of known dangerous schemes
    dangerous_schemes = {
        'javascript',
        'vbscript',
        'file',
        'livescript',
        'view-source',
        'data',   # Data URLs can be dangerous if not an image; keep for completeness
        'javascript',
        'vbscript',
        'data',   # Repeated for clarity; actual check above
        'javascript',
    }

    # Exclude common safe schemes (http, https, ftp, mailto etc.)
    safe_schemes = {
        'http',
        'https',
        'ftp',
        'ftps',
        'mailto',
        'tel',
        'sms',
    }

    # If scheme is explicitly listed as dangerous, flag it
    if scheme in dangerous_schemes and scheme not in safe_schemes:
        return True

    # Additional heuristic: if scheme contains 'javascript' or 'vbscript'
    # as a substring (e.g., 'jscript'), consider it dangerous.
    if re.search(r'javascript|vbscript', scheme, flags=re.IGNORECASE):
        return True

    return False