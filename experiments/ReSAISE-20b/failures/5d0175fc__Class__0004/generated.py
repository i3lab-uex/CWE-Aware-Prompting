import re

# Pre‑compile a simple, non‑backtracking pattern that accepts any http or https URL
_URL_PATTERN = re.compile(r'^https?://\S+$', re.IGNORECASE)


def verify_path_format(address: str) -> bool:
    """
    Verify that *address* is a syntactically valid http or https URL.

    The function uses a straightforward regular expression that matches
    strings starting with "http://" or "https://", followed by one or more
    non‑whitespace characters.  It deliberately avoids complex constructs
    that could trigger catastrophic backtracking, thereby mitigating
    CWE‑407.

    Parameters
    ----------
    address : str
        The input string to validate as a URL path.

    Returns
    -------
    bool
        True if *address* matches the pattern, False otherwise.
    """
    # A simple truthy check – ``re.match`` will return None if no match
    return bool(_URL_PATTERN.match(address))