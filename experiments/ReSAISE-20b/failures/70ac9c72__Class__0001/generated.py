import re

# Regular expression that matches a valid HTTP or HTTPS URL.
# It allows:
#   * http:// or https://
#   * a non-empty host (letters, digits, hyphens, dots)
#   * optional port
#   * an optional path/query/fragment that does not contain whitespace.
_URL_REGEX = re.compile(
    r'^(https?://)'          # http:// or https://
    r'([a-zA-Z0-9.-]+)'      # host (letters, digits, dots, hyphens)
    r'(:\d+)?'               # optional port
    r'(\/[^\s]*)?$'          # optional path (no whitespace)
)

def check_path(input_path: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the input matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non-string inputs; return False rather than raising an exception
    if not isinstance(input_path, str):
        return False

    # The regex is anchored; re.match will only succeed if the entire string matches
    return bool(_URL_REGEX.match(input_path))