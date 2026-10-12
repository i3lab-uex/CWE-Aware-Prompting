import re

# Pre‑compiled, simple pattern that matches a typical HTTP/HTTPS URL.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (https?)://                         # scheme and ://
    [A-Za-z0-9.-]+                      # hostname (letters, digits, dots, hyphens)
    (?::\d+)?                           # optional :port
    (?:/[^\s]*)?                        # optional path/query/hash, no whitespace allowed
    $                                   # end of string
    """,
    re.VERBOSE,
)

def verify_path_format(address: str) -> bool:
    """
    Return True if *address* is a valid http or https URL, otherwise False.
    No exceptions are raised; invalid input simply returns False.

    Parameters
    ----------
    address : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if the address matches the pattern, False otherwise.
    """
    if not isinstance(address, str):
        return False
    # Using fullmatch ensures the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(address))