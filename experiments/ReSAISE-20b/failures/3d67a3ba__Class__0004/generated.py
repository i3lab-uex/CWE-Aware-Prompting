import re

# A reasonably strict but efficient URL pattern.
_URL_REGEX = re.compile(
    r"""
    ^(?:(?:https?|ftp)://)?                # optional scheme
    (?:\S+(?::\S*)?@)?                    # optional username:password@
    (?:                                   # host
        (?P<ip>\d{1,3}(?:\.\d{1,3}){3})|  # IPv4
        (?P<hostname>(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})   # domain
    )
    (?::(?P<port>\d{1,5}))?                # optional port
    (?:/[^?#\s]*)?                         # optional path
    (?:\?[^\#\s]*)?                        # optional query
    (?:\#[^\s]*)?$                         # optional fragment
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid URL, otherwise False.
    
    The function uses a precompiled regular expression with no backtracking
    vulnerabilities and does not raise exceptions on invalid input.
    """
    if not isinstance(link, str):
        return False
    # Use fullmatch to ensure the entire string matches the pattern.
    return bool(_URL_REGEX.fullmatch(link))