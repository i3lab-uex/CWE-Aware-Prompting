import re

# A reasonably strict regex for HTTP/HTTPS URLs.
_URL_RE = re.compile(
    r'^(?:http|https)://'                         # protocol
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+'  # subdomains
    r'[A-Za-z]{2,6}'                              # TLD
    r'(?:\:\d{1,5})?'                             # optional port
    r'(?:/[^ \t\n\r\f\v]*)?$',                    # path/query/hash
    re.IGNORECASE
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid HTTP or HTTPS URL, False otherwise.
    No exception will be raised; an empty string is considered invalid.
    """
    if not isinstance(link, str) or not link:
        return False
    return bool(_URL_RE.fullmatch(link))