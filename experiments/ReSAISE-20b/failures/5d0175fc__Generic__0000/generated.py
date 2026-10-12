import re

# Regular expression pattern that matches a valid HTTP or HTTPS URL.
# It allows:
#   - scheme: http or https
#   - optional user:pass@
#   - hostname (IPv4, IPv6 or domain)
#   - optional port
#   - optional path, query string and fragment.
_URL_REGEX = re.compile(
    r'^(?:(?:http|https)://)'
    r'(?:[A-Za-z0-9_\-\.~!$&\'()*+,;=:@%]+@)?'          # optional userinfo
    r'(?:\[[A-Fa-f0-9:]+\]|'                           # IPv6
    r'(?:[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?'
    r'(?:\.[A-Za-z]{2,})+))'                          # domain
    r'(?::\d{1,5})?'                                   # optional port
    r'(?:/[A-Za-z0-9_\-\.~!$&\'()*+,;=:@%]*)*'         # path
    r'(?:\?[A-Za-z0-9_\-\.~!$&\'()*+,;=:@%]*)?'        # query
    r'(?:#[A-Za-z0-9_\-\.~!$&\'()*+,;=:@%]*)?'        # fragment
    r'$', re.IGNORECASE)

def verify_path_format(address: str) -> bool:
    """
    Verify whether the given string is a syntactically valid HTTP or HTTPS URL.

    Parameters
    ----------
    address : str
        The string to validate as a path.

    Returns
    -------
    bool
        True if the address matches the HTTP/HTTPS pattern, False otherwise.
    """
    if not isinstance(address, str):
        return False
    # Using fullmatch ensures the entire string matches the pattern.
    try:
        return bool(_URL_REGEX.fullmatch(address))
    except Exception:
        # Any unexpected error (e.g., regex engine failure) results in False.
        return False