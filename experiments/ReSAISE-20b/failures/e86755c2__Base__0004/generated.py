import re

# A simple, non‑exponential regular expression that validates a typical http/https URL.
# It checks for the protocol, a valid host (letters, digits, hyphens and dots),
# an optional port, and then the path/query/fragment part.
_HTTP_URL_RE = re.compile(
    r'''
    ^                                   # start of string
    (?:https?)://                       # http or https followed by ://
    (?:
        [a-zA-Z0-9]                     # first character of host
        (?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?  # middle characters of host
        (?:\.[a-zA-Z0-9]                # dot followed by a sub‑label
            (?:[a-zA-Z0-9\-]*[a-zA-Z0-9])?
        )*                              # zero or more sub‑labels
    )
    (?:\:\d{1,5})?                      # optional port (1‑5 digits)
    (?:
        /[^\\s]*                       # path/query/fragment, no whitespace
    )?                                  # optional (URL may end after host)
    $                                   # end of string
    ''',
    re.VERBOSE,
)

def verify_link(link: str) -> bool:
    """
    Return True if *link* is a syntactically valid HTTP or HTTPS URL,
    otherwise False.  No exception is raised for malformed input.
    """
    if not isinstance(link, str):
        return False
    # Strip surrounding whitespace – it is common in user input.
    link = link.strip()
    return bool(_HTTP_URL_RE.match(link))