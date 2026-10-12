import re

# Compile a simple, non‑backtracking regex that matches HTTP/HTTPS URLs.
# The pattern is intentionally minimal to avoid catastrophic backtracking
# (CWE‑1333). It only checks the scheme and ensures there are no whitespace
# characters in the rest of the string.
_URL_RE = re.compile(r'^(https?://)[^\s]+$')

def is_valid_path(site_path: str) -> bool:
    """
    Return True if `site_path` is a syntactically valid HTTP or HTTPS URL.
    
    The function performs a quick regex check for the scheme and ensures
    that no whitespace characters appear in the URL. No exceptions are raised.
    
    Args:
        site_path: The string to validate as a potential HTTP/HTTPS URL.
    
    Returns:
        bool: True if the string matches the expected pattern, False otherwise.
    """
    # Reject non‑string inputs gracefully
    if not isinstance(site_path, str):
        return False

    # Strip surrounding whitespace to avoid accidental false negatives
    stripped = site_path.strip()
    
    # Use the compiled regex for a fast, non‑backtracking match
    return bool(_URL_RE.match(stripped))