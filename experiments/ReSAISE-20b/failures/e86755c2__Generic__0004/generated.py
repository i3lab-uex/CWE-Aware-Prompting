import re

# Regular expression for a basic HTTP/HTTPS URL.
# It checks that the string starts with http:// or https://,
# followed by a non‑empty hostname (allowing IPv4, IPv6, or domain names),
# and optionally a path/query/fragment without whitespace.
_URL_RE = re.compile(
    r"""
    ^                               # start of string
    https?://                       # http or https scheme
    (?:
        # IPv4 address
        (?:\d{1,3}\.){3}\d{1,3}
      | # IPv6 address
        \[([0-9a-fA-F:]+)\]
      | # domain name
        (?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}
    )
    (?:
        /[^ \t\n\r]*            # optional path/query/fragment
    )?$
    """,
    re.VERBOSE,
)

def verify_link(link: str) -> bool:
    """
    Return True if `link` is a valid HTTP or HTTPS URL, otherwise False.
    
    Parameters
    ----------
    link : str
        The string to validate as a URL.
        
    Returns
    -------
    bool
        True if the input matches the expected HTTP/HTTPS URL pattern.
    """
    # Ensure the argument is a string; if not, return False gracefully.
    if not isinstance(link, str):
        return False
    # Strip surrounding whitespace to avoid false negatives.
    link = link.strip()
    return bool(_URL_RE.match(link))