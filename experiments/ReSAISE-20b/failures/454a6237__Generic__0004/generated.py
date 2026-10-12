import re

# Regular expression to match a valid http or https URL.
# It allows:
#   - http:// or https:// prefix
#   - any non-whitespace characters thereafter (basic validation)
_URL_RE = re.compile(r'^https?://[^\s]+$', re.IGNORECASE)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether the given string is a valid http or https URL.

    Parameters
    ----------
    path_string : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if the string matches the http/https pattern, False otherwise.
    """
    # Guard against non-string input; return False rather than raising an exception
    if not isinstance(path_string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    return bool(_URL_RE.fullmatch(path_string))