import re

# Pre‑compile the regular expression for efficiency and to avoid recompilation on each call.
# This pattern matches strings that start with http:// or https:// followed by at least one non‑whitespace character.
_URL_PATTERN = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the supplied string is a valid HTTP or HTTPS URL.

    The function uses a simple regular expression to check that the string
    starts with "http://" or "https://", followed by one or more non‑whitespace
    characters.  No exceptions are raised; any error in matching simply results
    in a return value of False.

    Parameters
    ----------
    site_path : str
        The string to be evaluated as a potential valid URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, otherwise False.
    """
    # Guard against non‑string input silently
    if not isinstance(site_path, str):
        return False

    # Perform the match; any error will be caught and treated as a non‑match
    try:
        return bool(_URL_PATTERN.match(site_path))
    except Exception:
        # In the unlikely event that matching raises an exception,
        # we consider it invalid rather than propagating the error.
        return False