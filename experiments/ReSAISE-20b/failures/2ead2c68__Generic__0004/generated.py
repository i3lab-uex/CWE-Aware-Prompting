import re

# Regular expression that matches a typical HTTP/HTTPS path.
# It starts with '/' and may contain alphanumerics, hyphens,
# underscores, dots, tildes, and the common URL reserved characters.
_PATH_RE = re.compile(
    r'^/'                                   # path must start with a slash
    r'(?:(?:[A-Za-z0-9\-._~]|[!$&\'()*+,;=:@/?%])*)$',
    re.ASCII
)

def path_verification(link: str) -> bool:
    """
    Check whether the provided string is a valid HTTP/HTTPS path.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if `link` matches the expected path pattern, False otherwise.
    """
    # Quick sanity check: if link is not a string or empty, return False
    if not isinstance(link, str) or not link:
        return False

    # Use the precompiled regex to test the path.
    return bool(_PATH_RE.match(link))