import re

# Pre‑compiled regex pattern for validating URLs.
# The pattern allows optional http:// or https://, a domain name (with at least one dot),
# an optional port number, and an optional path/query fragment.
_URL_PATTERN = re.compile(
    r'^(https?://)?'                     # optional scheme
    r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'    # domain (e.g., example.com)
    r'(?:\:[0-9]{1,5})?'                # optional port
    r'(?:/[^\s]*)?$'                    # optional path/query/fragment
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid URL, False otherwise.
    
    Parameters
    ----------
    link : str
        The string to validate as a URL.

    Returns
    -------
    bool
        True if the link matches the URL pattern, False otherwise.
    """
    # Ensure the input is a string; if not, return False gracefully.
    if not isinstance(link, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_PATTERN.fullmatch(link))