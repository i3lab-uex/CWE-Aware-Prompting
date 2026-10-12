import re

def analyze_scheme(url: str) -> bool:
    """
    Detect if the supplied string contains a potentially dangerous URL scheme
    (e.g. javascript:, vbscript:, data: but not image data URLs).

    Parameters
    ----------
    url : str
        The string to examine.

    Returns
    -------
    bool
        True if a dangerous scheme is detected; False otherwise.
    """
    # Normalise to lower case and strip leading whitespace
    url = url.lstrip().lower()

    # Regular expression to capture the scheme preceding a colon
    # Scheme must start with a letter and may contain letters, digits,
    # plus (+), hyphen (-) or period (.)
    scheme_match = re.match(r'^([a-z][a-z0-9+\-.]*):', url, flags=re.IGNORECASE)
    if not scheme_match:
        return False  # No scheme found

    scheme = scheme_match.group(1)

    # List of known dangerous schemes
    dangerous_schemes = {
        'javascript',
        'vbscript',
        'data',  # data: is dangerous unless it is an image
    }

    if scheme not in dangerous_schemes:
        return False

    # Exclude valid image data URLs
    if scheme == 'data' and url.startswith('data:image/'):
        return False

    # Anything else in the dangerous set is considered harmful
    return True