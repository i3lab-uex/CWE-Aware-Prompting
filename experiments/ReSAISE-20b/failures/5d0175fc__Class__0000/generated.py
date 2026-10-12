import re

# Pre‑compile a robust, non‑backtracking regex for HTTP/HTTPS URLs.
_URL_REGEX = re.compile(
    r'^(?P<scheme>https?)://'          # http or https
    r'(?P<host>[a-zA-Z0-9.-]+)'        # host (simplified)
    r'(?::\d{1,5})?'                  # optional port
    r'(?P<path>/[^\s?#]*)?'           # path component
    r'(\?[^\s#]*)?'                   # optional query string
    r'(#[^\s]*)?$',                   # optional fragment
    re.IGNORECASE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify that a given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches a valid http/https URL format,
        False otherwise.
    """
    if not isinstance(address, str):
        return False

    # Use fullmatch to ensure the entire string matches the pattern.
    match = _URL_REGEX.fullmatch(address.strip())
    return bool(match)