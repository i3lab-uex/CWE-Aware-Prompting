import re

# A reasonably strict, but not overly complex URL pattern.
# It matches http/https schemes, optional authentication,
# domain or IP, optional port, and path/query/hash.
_URL_REGEX = re.compile(
    r"""
    ^                           # start of string
    (?:https?://)               # scheme: http or https
    (?:[\w\-]+(?::[\w\-]+)?@)?  # optional user:pass@
    (?:                         # host
        (?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})  # domain
        |                           # or
        \d{1,3}(?:\.\d{1,3}){3}     # IPv4
    )
    (?::\d{2,5})?               # optional port
    (?:/[^\s]*)?                # optional path, query or fragment
    $                           # end of string
    """,
    re.VERBOSE | re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Verify whether the given string is a valid HTTP/HTTPS URL.

    Parameters
    ----------
    link : str
        The string to validate.

    Returns
    -------
    bool
        True if `link` matches the URL pattern, False otherwise.
    """
    if not isinstance(link, str):
        return False
    # Strip surrounding whitespace to avoid accidental mismatches.
    stripped = link.strip()
    return bool(_URL_REGEX.match(stripped))