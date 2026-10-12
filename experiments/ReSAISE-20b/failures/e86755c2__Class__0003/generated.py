import re

# Pre‑compile a safe, efficient regular expression that matches typical HTTP/HTTPS URLs.
# The pattern checks for the protocol (http or https), a non‑empty host, and an optional path.
# It deliberately avoids excessive backtracking by using atomic groups and
# limiting the character set for each component.
_URL_RE = re.compile(
    r'''
    ^                                   # start of string
    https?://                           # http or https scheme, followed by ://
    (?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?   # first label of hostname
    (?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*   # additional labels
    |\[[0-9a-fA-F:]+\]                 # or IPv6 literal in brackets
    )
    (?::\d{1,5})?                       # optional port (0-65535)
    (?:/[^\s]*)?$                        # optional path/query/fragment, no whitespace
    ''',
    re.VERBOSE | re.IGNORECASE,
)

def verify_link(link: str) -> bool:
    """
    Determine whether *link* is a syntactically valid HTTP or HTTPS URL.

    The function uses a pre‑compiled regular expression that
    matches the scheme, host (domain or IPv6), optional port,
    and an optional path/query/fragment.  No exceptions are raised
    – the function simply returns False for any non‑matching input.

    Args:
        link: The string to be evaluated as a potential URL.

    Returns:
        bool: True if *link* matches the expected pattern, otherwise False.
    """
    if not isinstance(link, str):
        return False
    # Using fullmatch ensures the entire string conforms to the pattern.
    return bool(_URL_RE.fullmatch(link))