import re

# Regular expression for a simple http or https URL.
# It matches:
#   - the scheme (http:// or https://)
#   - a host consisting of letters, digits, dots or hyphens
#   - an optional port (e.g., :8080)
#   - an optional path/query/fragment part that does not contain whitespace
#
# The pattern is anchored (^ and $) to avoid partial matches.
_URL_REGEX = re.compile(
    r"""^
        https?://                         # http:// or https://
        [A-Za-z0-9.-]+                    # host (letters, digits, dots, hyphens)
        (?::\d+)?                         # optional :port
        (?:/[^ \t\r\n]*)?                 # optional path/query/fragment, no whitespace
        $""",
    re.VERBOSE,
)

def path_check(u: str) -> bool:
    """
    Check whether the input string `u` is a valid http or https URL.

    Parameters
    ----------
    u : str
        The string to validate.

    Returns
    -------
    bool
        True if `u` matches the URL pattern, False otherwise.
    """
    try:
        # Use fullmatch to ensure the entire string conforms to the pattern
        return bool(_URL_REGEX.fullmatch(u))
    except Exception:
        # Any unexpected error is treated as a failed validation
        return False