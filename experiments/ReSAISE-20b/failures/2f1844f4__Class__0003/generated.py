import re

# Compile the regular expression once for efficiency.
# This pattern matches URLs that start with http:// or https://
# followed by any non-whitespace characters (i.e. the rest of the path).
_URL_RE = re.compile(r'^https?://[^\s]+$')

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP/HTTPS URL path.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    """
    # Defensive programming: ensure input is a string.
    if not isinstance(site_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(site_path))