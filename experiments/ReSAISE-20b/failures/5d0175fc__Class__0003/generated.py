import re

# Compile a safe, anchored regex pattern for http/https URLs.
# The pattern matches:
#   - scheme: http or https
#   - "://"
#   - a non-empty hostname (letters, digits, hyphens, dots)
#   - optional port
#   - optional path/query/fragment
#
# The pattern avoids nested quantifiers that could cause catastrophic backtracking.
_URL_PATTERN = re.compile(
    r"""
    ^                           # start of string
    (?:http|https)://           # scheme
    [a-zA-Z0-9.-]+              # hostname (simplified)
    (?::\d{1,5})?               # optional port
    (?:/[^\s]*)?                # optional path, query or fragment
    $                           # end of string
    """,
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify that the given string is a valid HTTP or HTTPS URL path.

    Parameters
    ----------
    address : str
        The string to validate.

    Returns
    -------
    bool
        True if the address matches the expected pattern, False otherwise.

    Notes
    -----
    - The function uses a precompiled regular expression with anchored
      patterns to avoid catastrophic backtracking.
    - No exceptions are raised; invalid input simply results in False.
    """
    if not isinstance(address, str):
        return False
    return bool(_URL_PATTERN.fullmatch(address))