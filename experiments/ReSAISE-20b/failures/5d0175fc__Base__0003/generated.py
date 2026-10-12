import re

# Compile a simple, non‑catastrophic regex for HTTP/HTTPS URLs.
# It matches the scheme followed by "://", then at least one non‑space
# character. The pattern is deliberately minimal to avoid excessive backtracking.
_URL_REGEX = re.compile(r'^(https?://\S+)$', re.IGNORECASE)

def verify_path_format(address: str) -> bool:
    """
    Verify whether the supplied string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate.

    Returns
    -------
    bool
        True if the address matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non‑string input silently: return False instead of raising.
    if not isinstance(address, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_REGEX.fullmatch(address))