import re

# Compile the regex once, using a simple and efficient pattern.
# This matches URLs that start with http:// or https:// followed by
# at least one non‑space character.  The pattern avoids nested quantifiers
# and backtracking pitfalls, mitigating CWE‑1333.
_URL_RE = re.compile(r'^(https?://[^\s]+)$', re.IGNORECASE)


def check_path(input_path: str) -> bool:
    """
    Determine whether *input_path* is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to be evaluated as a potential valid URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Guard against non-string input to avoid accidental crashes.
    if not isinstance(input_path, str):
        return False

    # Strip surrounding whitespace that might have been added inadvertently.
    trimmed = input_path.strip()

    # Use the pre‑compiled regex for efficient matching.
    return bool(_URL_RE.match(trimmed))