import re

# Regular expression that matches a typical HTTP or HTTPS URL.
# It checks for the scheme, "://", and ensures there is at least one
# non‑space character following it.  The pattern does not enforce a
# specific host or path format beyond the basic structure, making it
# suitable for quick validation without raising exceptions.
_URL_RE = re.compile(
    r'^https?://'          # http:// or https://
    r'[^ \t\n\r\f\v]+'     # at least one non‑whitespace character
)

def verify_path_format(address: str) -> bool:
    """
    Verify that the supplied string is a syntactically valid HTTP/HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    if not isinstance(address, str):
        return False
    return bool(_URL_RE.match(address))