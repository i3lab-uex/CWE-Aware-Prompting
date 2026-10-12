import re

# Precompiled regular expression that matches a simple HTTP/HTTPS URL.
# It allows any non-whitespace characters after the scheme.
_URL_RE = re.compile(r'^https?://[^\s]+$')

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    # Ensure that link is a string; if not, return False without raising.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))