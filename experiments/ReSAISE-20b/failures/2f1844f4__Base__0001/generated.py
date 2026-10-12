import re

# Pre‑compile a safe, non‑backtracking regex for HTTP/HTTPS URLs.
# The pattern matches the scheme (http or https), "://", and then any
# non‑whitespace characters up to the end of the string.
_URL_RE = re.compile(r'^https?://[^\s]+$')

def is_valid_path(site_path: str) -> bool:
    """
    Determine whether the provided string is a valid HTTP or HTTPS URL.

    The function uses a pre‑compiled regular expression that
    matches the scheme (http or https) followed by '://'
    and any sequence of non‑whitespace characters.
    It returns True if the entire string matches this pattern,
    otherwise False.

    Args:
        site_path: The URL candidate to validate.

    Returns:
        bool: True if `site_path` is a syntactically valid HTTP/HTTPS URL,
              False otherwise.
    """
    if not isinstance(site_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(site_path))