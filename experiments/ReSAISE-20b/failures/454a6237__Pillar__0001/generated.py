import re

# Regular expression pattern to validate http or https URLs.
# It allows:
#   - scheme: http:// or https://
#   - host (letters, digits, hyphens, dots)
#   - optional port
#   - optional path/query fragments consisting of common URL characters.
_URL_PATTERN = re.compile(
    r"""^
    https?://                                   # http:// or https://
    (?:[a-zA-Z0-9\-\.]+)                         # hostname or IP
    (?:\:[0-9]{1,5})?                            # optional port
    (?:/[^\s]*)?                                 # optional path/query
    $""",
    re.VERBOSE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Validate whether the given string is a well‑formed HTTP/HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate.

    Returns
    -------
    bool
        True if `path_string` matches the URL pattern, False otherwise.
    """
    try:
        return bool(_URL_PATTERN.fullmatch(path_string))
    except Exception:
        # Any unexpected error (e.g., None input) results in a False return.
        return False