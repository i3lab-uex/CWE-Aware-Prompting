import re

# Regular expression to validate a HTTP/HTTPS URL.
# It checks:
#   - scheme: http or https
#   - "://"
#   - non-empty host (no whitespace, at least one character)
#   - optional path/query/fragment
_URL_RE = re.compile(
    r'^(?i)https?://[^\s/$.?#].[^\s]*$',
    re.IGNORECASE
)

def check_path(input_path: str) -> bool:
    """
    Return True if `input_path` is a syntactically valid HTTP or HTTPS URL,
    otherwise False.

    Parameters
    ----------
    input_path : str
        The string to be evaluated as a potential valid path.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS URL pattern, False otherwise.
    """
    # Ensure input is a string; if not, treat as invalid without raising an exception.
    if not isinstance(input_path, str):
        return False

    # Strip leading/trailing whitespace to avoid false negatives.
    trimmed = input_path.strip()

    return bool(_URL_RE.match(trimmed))