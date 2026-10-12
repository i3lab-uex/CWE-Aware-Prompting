import re

# Compile a simple, non‑catastrophic regular expression that matches an HTTP(S) URL.
# The pattern:
#   - starts with http:// or https://
#   - followed by one or more non‑space characters for the host (no slashes)
#   - optionally followed by a slash and any non‑space characters for the path
_URL_REGEX = re.compile(r'^(https?://[^/\s]+(?:/[^\s]*)?)$', re.IGNORECASE)

def check_path(input_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS URL.

    The function uses a pre‑compiled regular expression that matches
    URLs of the form:
        http://hostname[/path]
        https://hostname[/path]

    Parameters
    ----------
    input_path : str
        The string to test.

    Returns
    -------
    bool
        True if the input matches the URL pattern, False otherwise.

    Notes
    -----
    - The function does not raise any exceptions.
    - The regex is deliberately simple to avoid catastrophic backtracking
      (CWE-407).
    """
    try:
        return bool(_URL_REGEX.match(input_path))
    except Exception:  # pragma: no cover
        # Any unexpected error (unlikely with a pre‑compiled regex) results in False.
        return False