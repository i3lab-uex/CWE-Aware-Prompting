import re

# Compile the regular expression once to avoid repeated compilation overhead.
# The pattern matches strings that start with "http://" or "https://",
# followed by one or more non-whitespace characters.
_HTTP_PATH_RE = re.compile(r'^https?://\S+$', flags=re.IGNORECASE)

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether `site_path` is a valid HTTP or HTTPS URL.

    The function uses a precompiled regular expression to check that the
    string starts with "http://" or "https://", and is followed by at least
    one non-whitespace character. No exceptions are raised; the function
    simply returns False for any input that does not match the pattern.

    Parameters
    ----------
    site_path : str
        The string to validate as a URL path.

    Returns
    -------
    bool
        True if `site_path` matches the HTTP/HTTPS pattern, otherwise False.
    """
    # Guard against non-string input; treat anything that is not a str as invalid
    if not isinstance(site_path, str):
        return False

    # Perform a full match; re.fullmatch would also work but using ^ and $ keeps
    # the compiled pattern simple and avoids potential backtracking issues.
    return bool(_HTTP_PATH_RE.match(site_path))