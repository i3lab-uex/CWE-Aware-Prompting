import re

# Compile a safe, non‑capturing regex for http/https URLs.
# The pattern allows any non-whitespace characters after the scheme
# and anchors to start/end of string.
_URL_REGEX = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def check_path_validity(path_string: str) -> bool:
    """
    Validate that the given string is a well‑formed HTTP or HTTPS URL.

    The function uses a simple regular expression that checks:
      * the string starts with "http://" or "https://"
      * it contains at least one character after the scheme
      * there are no whitespace characters in the URL

    Parameters
    ----------
    path_string : str
        The string to validate.

    Returns
    -------
    bool
        True if `path_string` matches the pattern, False otherwise.
    """
    # Guard against non-string inputs
    if not isinstance(path_string, str):
        return False

    # Perform the regex match; return True if it succeeds.
    return bool(_URL_REGEX.match(path_string))