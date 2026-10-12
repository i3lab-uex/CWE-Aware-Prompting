import re

# RFC 3986 compliant regex for common URL schemes (http, https, ftp)
_URL_PATTERN = re.compile(
    r'^(?:https?|ftp)://'                     # scheme
    r'(?:[A-Za-z0-9$_.+!*\'(),;?&=-]|%[0-9A-Fa-f]{2})+'  # userinfo or host
    r'(?:\:[0-9]+)?'                         # optional port
    r'(?:/[^ \t\n\r\f\v]*)?$'                # path, query and fragment
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid URL, otherwise False.
    
    The function uses a regular expression that covers the most common
    URL forms (http, https and ftp).  It intentionally does not perform
    DNS resolution or network access – it only checks the structure.
    
    Parameters
    ----------
    link : str
        The string to validate as a URL.
        
    Returns
    -------
    bool
        True if the string matches the URL pattern, False otherwise.
    
    Notes
    -----
    - The function is tolerant of percent‑encoded characters in the host,
      path, query and fragment components.
    - It accepts URLs without a trailing slash (e.g. ``https://example.com``)
      and with any path/query/fragment part.
    - No exceptions are raised; non‑string inputs are treated as invalid
      and result in ``False``.
    """
    if not isinstance(link, str):
        return False
    # Strip surrounding whitespace to avoid false negatives
    link = link.strip()
    if not link:
        return False
    return bool(_URL_PATTERN.match(link))