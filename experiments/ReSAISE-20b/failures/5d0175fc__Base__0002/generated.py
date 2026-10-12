import re

# A simple, non-backtracking regex that validates http/https URLs.
# It ensures:
#   • The scheme is either http or https
#   • Followed by :// and at least one non-whitespace character
#   • The rest of the URL can contain any characters except whitespace.
# This pattern avoids complex constructs that could lead to catastrophic backtracking
# (CWE-1333).
_URL_REGEX = re.compile(
    r"^(https?)://[^\s/]+(?:/[^\s]*)?$",
    re.IGNORECASE
)

def verify_path_format(address: str) -> bool:
    """
    Verify whether the given string is a valid HTTP or HTTPS path.

    Parameters
    ----------
    address : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the expected HTTP/HTTPS format,
        False otherwise.

    Notes
    -----
    The function performs a single regex match and does not raise any
    exceptions. It is intentionally conservative to avoid security issues
    such as catastrophic backtracking.
    """
    if not isinstance(address, str):
        return False
    # Strip leading/trailing whitespace to avoid accidental matches.
    address = address.strip()
    return bool(_URL_REGEX.match(address))