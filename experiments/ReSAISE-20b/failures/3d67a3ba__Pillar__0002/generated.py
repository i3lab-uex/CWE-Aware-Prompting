import re

# Regular expression pattern that matches most common URL formats.
_URL_PATTERN = re.compile(
    r'^(?:https?://)?'                     # optional scheme
    r'(?:\S+(?::\S*)?@)?'                 # optional user:pass authentication
    r'(?:'                                # host part (IP or domain)
        r'(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+'  # subdomains
        r'[A-Za-z]{2,63}'                # top‑level domain
    r'|'                                  # or IP address
        r'\d{1,3}(?:\.\d{1,3}){3}'
    r')'
    r'(?::\d+)?'                          # optional port
    r'(?:/\S*)?'                          # optional path, query or fragment
    r'$',                                 # end of string
    re.IGNORECASE,
)

def check_url_format(link: str) -> bool:
    """
    Return True if `link` is a syntactically valid URL, False otherwise.
    
    The function performs no network I/O and never raises an exception
    regardless of the input. It uses a compiled regular expression to
    validate the structure of typical URLs.
    
    Parameters:
        link (str): The string to validate as a URL.
        
    Returns:
        bool: True if the input matches the URL pattern, False otherwise.
    """
    # Ensure that `link` is a string; if not, immediately return False.
    if not isinstance(link, str):
        return False
    
    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_URL_PATTERN.fullmatch(link))