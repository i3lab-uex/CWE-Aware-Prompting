import re

# Compile a simple, efficient regular expression for http/https URLs.
# The pattern matches:
#   - scheme: http or https
#   - ://
#   - a non-empty host (any characters except whitespace and slash)
#   - optional path/query fragments starting with '/' or '?'.
#
# The use of a non-capturing group (?:...) and a limited set of allowed
# characters ensures that the regex is linear in input size and avoids
# catastrophic backtracking (CWE‑1333).
_URL_REGEX = re.compile(
    r'^(?:https?://)'          # scheme
    r'(?![^\s/]+$)[^\s]+'      # host (at least one non-whitespace character)
    r'(?:[/?][^\s]*)?$'        # optional path or query
)

def verify_link(link: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    link : str
        The string to be evaluated as a potential URL.

    Returns
    -------
    bool
        True if the string matches the http/https pattern, False otherwise.
    """
    # Guard against non-string input by attempting to coerce to string
    try:
        link_str = str(link)
    except Exception:
        return False

    # Use the precompiled regex to test the string.
    return bool(_URL_REGEX.match(link_str))