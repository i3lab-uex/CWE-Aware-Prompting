import re

# Regular expression that matches a basic HTTP/HTTPS URL.
# It requires the scheme (http or https), followed by "://",
# then a valid hostname (letters, digits, hyphens, dots),
# optionally followed by a port and an optional path/query/fragment.
_URL_RE = re.compile(
    r'''
    ^                           # start of string
    https?://                   # http or https scheme
    (?:
        [a-zA-Z0-9.-]+          # hostname (letters, digits, dots, hyphens)
        |
        \[?[a-fA-F0-9:]+\]?     # IPv6 literal (optional brackets)
    )
    (?::\d{1,5})?               # optional port
    (?:[/?#][^\s]*)?            # optional path, query or fragment
    $                           # end of string
    ''',
    re.VERBOSE,
)

def verify_link(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP or HTTPS URL,
    otherwise return False. No exceptions are raised.

    Parameters
    ----------
    link : str
        The string to evaluate as a potential URL.

    Returns
    -------
    bool
        True if the link matches the expected pattern, False otherwise.
    """
    # Guard against None or non-string inputs
    if not isinstance(link, str):
        return False

    # Strip surrounding whitespace that might have been added inadvertently
    link = link.strip()

    # Perform a full match against the compiled regex
    return bool(_URL_RE.fullmatch(link))