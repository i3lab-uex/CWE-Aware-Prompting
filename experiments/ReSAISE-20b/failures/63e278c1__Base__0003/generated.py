import re

# Compile a simple, efficient regex that matches http or https URLs.
# The pattern ensures the scheme is correct and then allows any non-whitespace
# characters for the rest of the URL.  It avoids complex backtracking constructs.
_HTTP_URL_RE = re.compile(r'^(https?://)[^\s]+$', re.IGNORECASE)

def check_path(string: str) -> bool:
    """
    Return True if `string` is a valid http or https URL, False otherwise.
    
    The function never raises an exception: any error in the regex matching
    results in a False return value.
    
    Parameters
    ----------
    string : str
        The input string to validate as an HTTP/HTTPS URL.
    
    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    try:
        return bool(_HTTP_URL_RE.fullmatch(string))
    except Exception:  # pragma: no cover
        # Any unexpected error (e.g., invalid regex engine state) results in False.
        return False