import re

# Regular expression for a simple HTTP/HTTPS URL path.
# It matches the scheme followed by :// and then any non‑space characters.
_URL_RE = re.compile(r'^(?:http|https)://[^\s]+$', re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Check whether the supplied string is a valid HTTP/HTTPS path.

    Parameters
    ----------
    string : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non‑string input: simply return False.
    if not isinstance(string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(string))