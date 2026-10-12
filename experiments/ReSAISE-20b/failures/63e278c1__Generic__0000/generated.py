import re

# Regular expression for a basic HTTP/HTTPS URL.
# It matches strings that start with http:// or https://,
# followed by at least one non-whitespace character.
_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)

def check_path(string: str) -> bool:
    """
    Return True if `string` is a valid HTTP or HTTPS URL, otherwise False.

    Parameters
    ----------
    string : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    try:
        return bool(_URL_RE.match(string))
    except Exception:
        # In case of any unexpected error, do not raise – just return False.
        return False