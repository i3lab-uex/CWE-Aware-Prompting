import re

# A compact, non‑capturing regular expression that checks for a valid HTTP/HTTPS URL.
# It ensures:
#   • the scheme is http or https
#   • a non‑empty hostname (letters, digits, hyphens, dots)
#   • an optional port
#   • an optional path/query/fragment that does not contain whitespace.
_URL_REGEX = re.compile(
    r"""
    ^                           # start of string
    (?:https?://)               # scheme: http or https, followed by ://
    [a-zA-Z0-9.-]+              # hostname (letters, digits, dots, hyphens)
    (?::\d{1,5})?               # optional port (1‑5 digits)
    (?:/[^\s]*)?                # optional path, query or fragment
    $                           # end of string
    """,
    re.VERBOSE,
)

def check_url_format(link: str) -> bool:
    """
    Return True if *link* is a syntactically valid HTTP/HTTPS URL, False otherwise.
    No exceptions are raised; the function handles any input safely.

    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the link matches the pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False
    # Strip leading/trailing whitespace to avoid accidental failures.
    link = link.strip()
    return bool(_URL_REGEX.match(link))