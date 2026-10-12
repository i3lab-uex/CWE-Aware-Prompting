import re

# Compile a safe, non‑backtracking regex for HTTP/HTTPS URLs.
# It matches the scheme (http or https), followed by ://,
# then any non‑whitespace characters.  This is a very permissive
# check that will accept most valid URLs while avoiding complex
# patterns that could lead to catastrophic backtracking.
_URL_REGEX = re.compile(r'^(https?)://\S+$', flags=re.IGNORECASE)


def is_valid_path(site_path: str) -> bool:
    """
    Return True if `site_path` is a syntactically valid HTTP/HTTPS URL
    according to the simple regular expression defined above.  The
    function never raises an exception; any errors are caught and the
    function returns False.

    Parameters
    ----------
    site_path : str
        The string to test as a potential URL.

    Returns
    -------
    bool
        True if the input matches the pattern, False otherwise.
    """
    try:
        # Use fullmatch to ensure the entire string matches the pattern
        return bool(_URL_REGEX.fullmatch(site_path))
    except Exception:
        # In the unlikely event of an internal error, return False
        return False