import re

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Return True if the supplied URI contains a dangerous scheme (e.g. javascript:, vbscript:)
    but exclude safe image-based data URLs (data:image/...).

    Parameters
    ----------
    uri_str : str
        The URI string to test.

    Returns
    -------
    bool
        True if a dangerous scheme is present, False otherwise.
    """
    # Normalise whitespace and case for matching
    uri = uri_str.strip()

    # Quick exit if the string is empty after stripping
    if not uri:
        return False

    # Pattern to capture a scheme at the start of the string
    scheme_pattern = re.compile(r'^(?i)([a-z][a-z0-9+\-.]*):')

    match = scheme_pattern.match(uri)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Dangerous schemes list
    dangerous_schemes = {'javascript', 'vbscript'}

    if scheme in dangerous_schemes:
        return True

    # Handle data URIs – only flag if not an image
    if scheme == 'data':
        # Data URLs have the form data:[<mediatype>][;base64],<data>
        # We consider image/* safe. Anything else is dangerous.
        # Extract the media type if present
        try:
            mediatype_part = uri[5:].split(';', 1)[0]  # part after 'data:' up to first ';' or comma
        except Exception:
            mediatype_part = ''

        if mediatype_part.lower().startswith('image/'):
            return False
        else:
            return True

    # Any other scheme is considered safe for this check
    return False