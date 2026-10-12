import re

# Regular expression that matches a valid HTTP or HTTPS URL.
# It allows any non‑whitespace characters after the scheme.
_HTTP_URL_RE = re.compile(r'^https?://[^\s]+$', re.IGNORECASE)


def check_path(string: str) -> bool:
    """
    Return True if *string* is a syntactically valid HTTP/HTTPS URL,
    otherwise return False.

    The function never raises an exception; it simply returns a boolean.
    """
    if not isinstance(string, str):
        return False
    return bool(_HTTP_URL_RE.match(string))