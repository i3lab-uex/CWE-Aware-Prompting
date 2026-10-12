import re

# Regular expression to validate a URL that starts with http:// or https://
# The pattern allows any non‑whitespace characters after the scheme.
_HTTP_URL_RE = re.compile(
    r'^(https?://)'          # http or https scheme
    r'([^\s/$.?#].[^\s]*)$'  # rest of the URL (no whitespace)
)

def validate_path(path: str) -> bool:
    """
    Return True if `path` is a valid http or https URL, False otherwise.
    No exceptions are raised; any error results in False.

    Parameters
    ----------
    path : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches a valid http/https URL pattern, False otherwise.
    """
    # Ensure the input is a string; if not, return False immediately
    if not isinstance(path, str):
        return False

    # Perform a full match against the compiled regular expression
    return bool(_HTTP_URL_RE.fullmatch(path))