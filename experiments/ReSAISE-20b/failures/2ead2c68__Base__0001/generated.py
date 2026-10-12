import re

# Compile the regex once at module load to avoid repeated compilation.
_PATH_RE = re.compile(r'^https?://[^\s]+$')

def path_verification(link: str) -> bool:
    """
    Check if the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    # Guard against non-string inputs gracefully.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string matches the pattern.
    return bool(_PATH_RE.fullmatch(link))