import re

# Pre‑compile a simple, efficient regex for HTTP/HTTPS URLs.
# The pattern matches strings that start with "http://" or "https://"
# followed by at least one non‑whitespace character.
_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def path_check(u: str) -> bool:
    """
    Return True if the input string `u` is a valid HTTP/HTTPS URL path,
    otherwise return False. The function never raises exceptions.
    """
    try:
        # Fast path: use the pre‑compiled regex to test the string.
        return bool(_URL_RE.match(u))
    except Exception:
        # In case of any unexpected error (e.g., non‑string input),
        # return False instead of propagating the exception.
        return False