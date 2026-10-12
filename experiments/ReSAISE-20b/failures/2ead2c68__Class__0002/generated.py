import re

# Pre‑compiled regular expression that matches a valid HTTP or HTTPS path.
# It allows:
#   - the scheme (http:// or https://)
#   - a hostname consisting of alphanumerics, hyphens and dots
#   - an optional port
#   - a path composed of allowed URL characters (unreserved + sub-delims + :@)
#   - optional query and fragment parts
#
# The pattern is deliberately simple to avoid catastrophic backtracking.
_PATH_REGEX = re.compile(
    r'^(?:https?://)'                      # http:// or https://
    r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?'  # hostname label
    r'(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?)*'  # additional labels
    r')'
    r'(?:\:\d{1,5})?'                     # optional port
    r'(?P<path>/[^\s?#]*)?'                # path (no whitespace)
    r'(?:\?[^\s#]*)?'                     # optional query
    r'(?:#[^\s]*)?$'                      # optional fragment
)

def path_verification(link: str) -> bool:
    """
    Validate that the provided string is a well‑formed HTTP or HTTPS URL path.

    Parameters
    ----------
    link : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the input matches the expected pattern, False otherwise.
    """
    try:
        # Quick sanity check: empty or None input is invalid
        if not link or not isinstance(link, str):
            return False

        # Use fullmatch to ensure the entire string conforms to the pattern.
        return bool(_PATH_REGEX.fullmatch(link))
    except Exception:
        # Any unexpected exception is treated as an invalid path.
        return False