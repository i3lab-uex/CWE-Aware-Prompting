import re

# Regular expression that matches a simple HTTP/HTTPS URL.
# It checks for the scheme (http or https), followed by "://",
# and then one or more non‑whitespace characters.
_URL_RE = re.compile(r'^https?://\S+$', re.IGNORECASE)


def is_valid_path(site_path: str) -> bool:
    """
    Return True if `site_path` looks like a valid http or https URL,
    otherwise return False. No exceptions are raised.

    Args:
        site_path: The string to test.

    Returns:
        bool: True if the string matches a simple http/https URL pattern.
    """
    # Guard against None or non‑string inputs
    if not isinstance(site_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(site_path))