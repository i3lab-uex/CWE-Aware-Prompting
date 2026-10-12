import re

# A simple, non‑catastrophic regex that covers the most common URL forms.
_URL_RE = re.compile(
    r'^(?:(?:https?|ftp):\/\/)'      # protocol
    r'(?:\S+(?::\S*)?@)?'            # optional username:password@
    r'(?:[A-Za-z0-9.-]+|\[[^\]]+\])' # domain or IPv6 address
    r'(?:\:\d+)?'                    # optional port
    r'(?:\/[^\s]*)?$'                # optional path/query/hash, no spaces
)

def check_url_format(link: str) -> bool:
    """
    Validate a URL string using a precompiled regular expression.

    Parameters
    ----------
    link : str
        The input string to validate as a URL.

    Returns
    -------
    bool
        True if `link` matches the URL pattern, False otherwise.
    """
    return bool(_URL_RE.match(link))