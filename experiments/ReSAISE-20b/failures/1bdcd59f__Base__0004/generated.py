import re

# Compile a simple, non‑backtracking regex that matches an http or https URL
_URL_RE = re.compile(
    r'^(?:http|https)://'        # protocol
    r'[^\s/$.?#].[^\s]*$'       # minimal host and optional path/query
)

def path_check(u: str) -> bool:
    """
    Return True if *u* is a valid HTTP/HTTPS URL, False otherwise.
    
    The function uses a pre‑compiled regular expression that does not
    contain nested quantifiers, preventing exponential backtracking
    (CWE‑1333).  It also does not raise any exceptions for malformed input.
    
    Parameters
    ----------
    u : str
        The string to validate as a URL.
        
    Returns
    -------
    bool
        True if *u* matches the pattern, False otherwise.
    """
    try:
        # fullmatch ensures the entire string satisfies the regex
        return bool(_URL_RE.fullmatch(u))
    except Exception:
        # Defensive: in case something unexpected happens, return False
        return False