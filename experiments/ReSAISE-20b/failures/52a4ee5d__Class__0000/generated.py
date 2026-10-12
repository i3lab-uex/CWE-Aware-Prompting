import re

def detect_js_scheme(url_string: str) -> bool:
    """
    Detect whether a string contains a potentially dangerous URL scheme such as
    javascript:, vbscript:, or other non‑image data URLs.

    Parameters
    ----------
    url_string : str
        The string to examine for possible dangerous URL schemes.

    Returns
    -------
    bool
        True if the string starts with a hazardous scheme (excluding valid image data URLs),
        False otherwise.

    Notes
    -----
    * The function is case‑insensitive.
    * Leading whitespace is ignored.
    * Only the scheme part of a URL is examined; path/query components are not considered.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading whitespace and make case‑insensitive
    trimmed = url_string.lstrip()

    # Regular expression to capture the scheme part of a URL
    # We allow schemes that are letters, digits, plus, period, or hyphen.
    scheme_re = re.compile(r'^(?i)([a-z0-9.+-]+):')

    match = scheme_re.match(trimmed)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Ignore the special case of data:image URLs
    if scheme == 'data':
        # If it starts with 'data:' but not followed by 'image/', treat as dangerous
        data_match = re.match(r'^(?i)data:(?!image/)', trimmed)
        return bool(data_match)

    # Define known dangerous schemes
    dangerous_schemes = {
        'javascript',
        'vbscript',
        'data',          # data: URLs are dangerous unless image/
        'file',
        'ftp',
        'gopher',
        'mailto',       # some contexts treat mailto as dangerous
    }

    return scheme in dangerous_schemes