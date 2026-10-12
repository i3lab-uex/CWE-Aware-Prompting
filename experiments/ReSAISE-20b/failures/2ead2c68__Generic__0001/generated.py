import re

# Regular expression that matches a simple HTTP/HTTPS URL path.
# It allows an optional scheme (http:// or https://), a host part consisting
# of letters, digits, dots and hyphens, and an optional path that can contain
# any non‑whitespace characters (including query strings).
_URL_RE = re.compile(
    r'^(?:https?://)?'          # optional scheme
    r'[a-zA-Z0-9.-]+'           # host (letters, digits, dots, hyphens)
    r'(?:/[^\s]*)?$'            # optional path/query
)

def path_verification(link: str) -> bool:
    """
    Check whether the given string is a valid HTTP/HTTPS path.

    Parameters
    ----------
    link : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the input matches the pattern, False otherwise.
    """
    # Guard against non‑string inputs and strip surrounding whitespace
    if not isinstance(link, str):
        return False

    link = link.strip()
    # If the string is empty after stripping, it's not a valid URL
    if not link:
        return False

    # Perform the regex match; re.fullmatch ensures the entire string conforms.
    return bool(_URL_RE.fullmatch(link))