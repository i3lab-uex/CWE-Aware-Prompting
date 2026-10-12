import re

# Regular expression that matches a simple HTTP/HTTPS URL.
# It allows:
#   - http:// or https://
#   - a domain consisting of letters, digits, hyphens and dots
#   - an optional port number (1–5 digits)
#   - an optional path/query string composed of common URL characters
_URL_REGEX = re.compile(
    r'''
    ^                       # start of string
    (https?://)             # http:// or https://
    ([a-zA-Z0-9.-]+)        # domain name (letters, digits, hyphen, dot)
    (:([0-9]{1,5}))?        # optional port number
    (/[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]*)?  # optional path/query string
    $                       # end of string
    ''',
    re.VERBOSE,
)

def check_path(string: str) -> bool:
    """
    Return True if `string` is a valid HTTP or HTTPS URL according to
    the predefined regular expression; otherwise return False.
    
    The function never raises an exception. If `string` is not a
    string instance, it returns False.
    """
    if not isinstance(string, str):
        return False
    return bool(_URL_REGEX.fullmatch(string))