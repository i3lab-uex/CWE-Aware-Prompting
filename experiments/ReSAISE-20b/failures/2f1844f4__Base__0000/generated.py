import re

# Compile the regular expression once to avoid repeated compilation overhead.
# The pattern matches strings that start with http:// or https:// followed by
# at least one non-whitespace character. It is anchored to the start and end
# of the string, which prevents catastrophic backtracking.
_HTTP_PATH_RE = re.compile(r'^(https?://)[^\s]+$')

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the expected http/https path format,
        False otherwise.
    """
    # Return False immediately if input is not a string (defensive).
    if not isinstance(site_path, str):
        return False

    # Use the precompiled regex to test the string.
    return bool(_HTTP_PATH_RE.match(site_path))