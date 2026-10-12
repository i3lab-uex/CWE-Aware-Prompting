import re

# A safe, linear‑time regex that checks for a valid http/https URL.
# It matches:
#   - scheme: "http" or "https"
#   - "://"
#   - a non‑empty host (no whitespace)
#   - optional path/query/fragment that does not contain spaces
URL_PATTERN = re.compile(
    r"^(https?://)"          # scheme
    r"([^/\s]+)"             # host (at least one non‑space, non‑slash character)
    r"(/[^ \t\r\n]*)?$",     # optional path/query/fragment, no spaces
    re.IGNORECASE
)

def check_path_validity(path_string: str) -> bool:
    """
    Return True if `path_string` is a syntactically valid http or https URL,
    otherwise return False. No exception is raised.
    
    Parameters
    ----------
    path_string : str
        The URL string to validate.

    Returns
    -------
    bool
        True if the path is valid, False otherwise.
    """
    # Quick sanity check: must be a string
    if not isinstance(path_string, str):
        return False

    # Strip leading/trailing whitespace to avoid accidental failures
    trimmed = path_string.strip()
    if not trimmed:
        return False

    # Use the compiled regex to test validity
    return bool(URL_PATTERN.match(trimmed))