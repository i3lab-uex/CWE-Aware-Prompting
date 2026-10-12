import re

# Regular expression to validate an HTTP or HTTPS URL.
# It ensures the string starts with http:// or https://,
# followed by a non-empty host part, and optionally a path/query/fragment.
_URL_RE = re.compile(
    r"""
    ^                                   # start of string
    (https?)://                         # http or https scheme followed by ://
    (?:
        [A-Za-z0-9]                     # first character of host (alnum)
        (?:[A-Za-z0-9.-]*[A-Za-z0-9])? # rest of host (letters, digits, dots, hyphens)
    )
    (?:
        /                               # optional path start
        [^\s]*                          # any non‑space characters after the slash
    )?
    $                                   # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def verify_path_format(address: str) -> bool:
    """
    Verify that *address* is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if *address* matches the HTTP/HTTPS pattern, False otherwise.
    """
    if not isinstance(address, str):
        return False
    return bool(_URL_RE.match(address))