import re

# Regular expression that matches a valid http or https URL path.
# It allows:
# - The scheme (http:// or https://)
# - An optional host part (letters, digits, hyphens, dots)
# - Optional port
# - An optional path starting with '/' and containing allowed URL characters
# - Optional query string or fragment after '?' or '#'
_HTTP_URL_RE = re.compile(
    r"""^
        https?://                                   # http:// or https://
        (?:[a-zA-Z0-9\-\.]+)                         # hostname
        (?::\d{1,5})?                                # optional port
        (?:/[^?#]*)?                                 # optional path
        (?:\?[^\#]*)?                                # optional query string
        (?:#[^\s]*)?                                 # optional fragment
    $""",
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify if the given string is a syntactically valid http or https URL.

    Parameters
    ----------
    address : str
        The input string to validate as a path.

    Returns
    -------
    bool
        True if `address` matches the expected pattern, False otherwise.

    Notes
    -----
    - No exceptions are raised; invalid input simply results in False.
    - The function uses a precompiled regular expression to avoid
      unnecessary compilation overhead and potential resource leaks.
    """
    if not isinstance(address, str):
        # Non-string inputs are considered invalid
        return False

    # Use fullmatch to ensure the entire string matches the pattern.
    match = _HTTP_URL_RE.fullmatch(address)
    return bool(match)