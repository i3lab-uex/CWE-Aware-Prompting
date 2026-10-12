import re

# Compile the pattern once at module load to avoid repeated compilation overhead.
_LINK_PATTERN = re.compile(r'^https?://[^\s]+$')

def verify_link(link: str) -> bool:
    """
    Check whether the provided string is a valid HTTP or HTTPS URL.

    The function uses a simple regular expression that ensures the string
    starts with "http://" or "https://", followed by at least one non‑whitespace
    character.  This pattern is intentionally minimal to avoid catastrophic
    backtracking while still matching typical URL forms.

    Parameters
    ----------
    link : str
        The string to evaluate.

    Returns
    -------
    bool
        True if the string matches the pattern, False otherwise.
    """
    # Short‑circuit for non-string inputs to avoid unnecessary regex work.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_LINK_PATTERN.fullmatch(link))