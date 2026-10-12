import re

# Regular expression that matches a well‑formed HTTP or HTTPS URL.
# The pattern is intentionally written to avoid catastrophic backtracking
# by limiting quantifiers and using non‑capturing groups where possible.
_HTTP_URL_REGEX = re.compile(
    r"""^
        https?://                                 # http:// or https://
        (?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+   # domain name
        [a-zA-Z]{2,6}                              # top‑level domain
        (?:/[^?#\s]*)?                             # optional path
        (?:\?[^\#\s]*)?                            # optional query string
        (?:\#[^\s]*)?                              # optional fragment
    $""",
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Determine whether the given string is a valid HTTP or HTTPS URL.

    Parameters
    ----------
    input_path : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    # Defensive copy: strip leading/trailing whitespace to avoid accidental
    # mismatches due to surrounding spaces.
    cleaned = input_path.strip()
    return bool(_HTTP_URL_REGEX.fullmatch(cleaned))