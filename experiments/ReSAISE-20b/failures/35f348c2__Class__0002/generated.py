import re

# Regular expression for a valid http or https URL path.
# It matches:
#   - scheme: "http" or "https"
#   - "://"
#   - domain (letters, digits, hyphens, dots) with at least one dot
#   - optional port (e.g., :80)
#   - path starting with "/" and containing allowed URL characters
# The pattern is anchored to avoid partial matches.
_URL_PATTERN = re.compile(
    r'^https?://'                                 # http:// or https://
    r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+'  # subdomains
    r'[a-zA-Z]{2,}'                               # top-level domain
    r'(?::\d{1,5})?'                              # optional port (0-65535)
    r'(?:/[^\s]*)?$'                              # optional path, no spaces
)

def validate_path(path: str) -> bool:
    """
    Validate that the given string is a well‑formed http or https URL path.

    Parameters
    ----------
    path : str
        The input string to validate.

    Returns
    -------
    bool
        True if `path` matches the URL pattern, False otherwise.
    """
    # Quick length check to avoid unnecessary regex evaluation
    if not isinstance(path, str) or len(path) > 2048:
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return _URL_PATTERN.fullmatch(path) is not None