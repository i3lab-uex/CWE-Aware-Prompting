import re

# Regular expression to match a valid HTTP or HTTPS URL path.
# This pattern ensures the string starts with http:// or https://,
# followed by at least one non-whitespace character.
_HTTP_PATH_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Validate whether the given string is a valid HTTP/HTTPS path.

    Parameters
    ----------
    string : str
        The input string to validate.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS path pattern, False otherwise.
    """
    # Defensive programming: ensure input is a string
    if not isinstance(string, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern
    try:
        return _HTTP_PATH_RE.fullmatch(string) is not None
    except re.error:
        # In the unlikely event the regex fails to compile/run, treat as invalid
        return False