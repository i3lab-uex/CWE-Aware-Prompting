import re

# Pre-compiled regular expression for HTTP/HTTPS URLs.
# This pattern ensures the string starts with http:// or https://,
# followed by at least one non-whitespace character.
_HTTP_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)

def path_check(u: str) -> bool:
    """
    Validate whether a given string is a well-formed HTTP or HTTPS URL.

    Parameters
    ----------
    u : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non-string input to avoid unexpected exceptions.
    if not isinstance(u, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(u))