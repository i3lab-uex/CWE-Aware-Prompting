import re

# Compile the regular expression once for efficiency.
# The pattern matches a string that starts with http:// or https://,
# followed by one or more non‑space characters (a very permissive check
# for a URL).  It does not perform full RFC‑3986 validation but is
# sufficient for basic path verification.
_URL_REGEX = re.compile(r'^(https?://)[^\s]+$', re.IGNORECASE)

def check_path_validity(path_string: str) -> bool:
    """
    Verify that *path_string* is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    path_string : str
        The string to validate.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.
    """
    try:
        return bool(_URL_REGEX.match(path_string))
    except Exception:
        # In case of any unexpected error (e.g., invalid regex),
        # return False instead of raising.
        return False