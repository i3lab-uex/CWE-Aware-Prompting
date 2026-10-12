import re

# Compile the regex once at import time to avoid repeated compilation.
# This pattern matches a basic HTTP/HTTPS URL with optional path, query and fragment.
# It is deliberately conservative to avoid catastrophic backtracking or excessive
# resource usage, thus mitigating CWE-664 concerns.
_URL_REGEX = re.compile(
    r"""
    ^                                   # start of string
    (https?)://                         # scheme http or https followed by ://
    [a-zA-Z0-9.-]+                      # domain (letters, digits, dot or hyphen)
    (?::\d{1,5})?                       # optional port (1-5 digits)
    (?:/[^\s?#]*)?                      # optional path
    (?:\?[^\s#]*)?                      # optional query string
    (?:#[^\s]*)?                        # optional fragment
    $                                   # end of string
    """,
    re.VERBOSE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Validate whether the given string is a syntactically correct HTTP/HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.

    Notes
    -----
    - No exceptions are raised; invalid inputs simply return False.
    - The regex is intentionally simple and safe to avoid excessive
      backtracking or denial‑of‑service vulnerabilities.
    """
    if not isinstance(path_string, str):
        return False
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_REGEX.fullmatch(path_string))