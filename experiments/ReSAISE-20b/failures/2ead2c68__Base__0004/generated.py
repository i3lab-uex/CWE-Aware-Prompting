import re

# A simple, non‑capturing regex that matches URLs beginning with http:// or https://
# followed by any number of non‑whitespace characters.
_HTTP_URL_RE = re.compile(r'^(?:http|https)://[^\s]+$', re.IGNORECASE)

def path_verification(link: str) -> bool:
    """
    Return True if *link* is a valid HTTP or HTTPS URL, False otherwise.
    
    The function uses a precompiled regular expression that checks the following
    conditions:
      * Starts with 'http://' or 'https://'.
      * Contains at least one non‑whitespace character after the scheme.
    
    The regex is deliberately simple to avoid catastrophic backtracking
    (CWE‑1333) and does not attempt to validate domain names or path components.
    
    Parameters
    ----------
    link : str
        The string to validate as an HTTP/HTTPS URL.
    
    Returns
    -------
    bool
        True if *link* matches the pattern, False otherwise.
    
    Notes
    -----
    This function does **not** raise exceptions.  It simply returns False for any
    input that is not a string or does not match the pattern.
    """
    if not isinstance(link, str):
        return False
    return bool(_HTTP_URL_RE.match(link))