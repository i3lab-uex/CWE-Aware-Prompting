import re

# Compile a safe, efficient regex for HTTP/HTTPS URLs.
# The pattern allows typical URL characters but rejects whitespace and
# uses a non‑capturing group for the scheme.
_URL_REGEX = re.compile(
    r'^(?:http|https)://'
    r'[A-Za-z0-9\-._~:/?#[\]@!$&\'()*+,;=%]+$',
    re.ASCII
)

def check_path(input_path: str) -> bool:
    """
    Determine whether a string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.

    Notes
    -----
    The function performs no exception handling beyond normal
    string operations.  It returns False for any input that does not
    match the pattern, ensuring no exception is raised during
    validation.
    """
    # Fast exit for non-string inputs
    if not isinstance(input_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_REGEX.fullmatch(input_path))