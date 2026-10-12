import re

# Regular expression to validate a simple HTTP/HTTPS URL.
# It matches:
#   - scheme http or https
#   - a domain consisting of labels separated by dots (at least one dot)
#   - optional port number
#   - an optional path that does not contain whitespace
_VALID_URL_RE = re.compile(
    r'^(https?://)'                     # http:// or https://
    r'(?:[a-zA-Z0-9-]+\.)+'             # one or more domain labels followed by a dot
    r'[a-zA-Z]{2,}'                     # top‑level domain (at least two letters)
    r'(?:\:\d+)?'                       # optional port
    r'(?:/[^\s]*)?$'                    # optional path that has no whitespace
)

def validate_path(path: str) -> bool:
    """
    Validate whether a given string is a well‑formed HTTP or HTTPS URL.

    Parameters
    ----------
    path : str
        The URL string to validate.

    Returns
    -------
    bool
        True if the input matches the expected pattern, False otherwise.
    """
    # The function must not raise exceptions; any errors are treated as invalid input.
    try:
        if not isinstance(path, str):
            return False
        # Strip surrounding whitespace to avoid false negatives.
        path = path.strip()
        if not path:
            return False
        # Use the compiled regex to check for a match.
        return bool(_VALID_URL_RE.match(path))
    except Exception:
        # Any unexpected error results in a False return value.
        return False